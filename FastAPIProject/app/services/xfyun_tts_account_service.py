from __future__ import annotations

import json
import os
from datetime import datetime
from threading import RLock
from uuid import uuid4

from app.core.config import settings
from app.models.schemas import XfyunTtsAccountUpsertRequest, XfyunTtsAccountView


class XfyunTtsAccountService:
    def __init__(self, store_path: str | None = None) -> None:
        self._store_path = store_path or settings.xfyun_account_store_path
        self._lock = RLock()
        self._last_mtime: float | None = None
        self._state = self._load_state()

    def list_accounts(self) -> list[XfyunTtsAccountView]:
        with self._lock:
            self._refresh_state_if_needed()
            accounts = self._state.get("accounts", [])
            active_account_id = self._state.get("activeAccountId")
            views: list[XfyunTtsAccountView] = []
            for account in accounts:
                views.append(
                    XfyunTtsAccountView(
                        accountId=account["accountId"],
                        name=account["name"],
                        appId=account["appId"],
                        apiKey=account["apiKey"],
                        apiSecret=account["apiSecret"],
                        defaultVcn=str(account.get("defaultVcn", "xiaoyan")).strip() or "xiaoyan",
                        description=account.get("description", ""),
                        enabled=bool(account.get("enabled", True)),
                        isActive=account["accountId"] == active_account_id,
                        updatedAt=self._parse_datetime(account.get("updatedAt")),
                    )
                )
            return views

    def get_active_account(self) -> XfyunTtsAccountView | None:
        with self._lock:
            self._refresh_state_if_needed()
            active_account_id = self._state.get("activeAccountId")
            if not active_account_id:
                return None

            for account in self._state.get("accounts", []):
                if account["accountId"] == active_account_id:
                    return XfyunTtsAccountView(
                        accountId=account["accountId"],
                        name=account["name"],
                        appId=account["appId"],
                        apiKey=account["apiKey"],
                        apiSecret=account["apiSecret"],
                        defaultVcn=str(account.get("defaultVcn", "xiaoyan")).strip() or "xiaoyan",
                        description=account.get("description", ""),
                        enabled=bool(account.get("enabled", True)),
                        isActive=True,
                        updatedAt=self._parse_datetime(account.get("updatedAt")),
                    )
            return None

    def upsert_account(self, request: XfyunTtsAccountUpsertRequest) -> XfyunTtsAccountView:
        normalized_name = request.name.strip()
        normalized_app_id = request.appId.strip()
        normalized_api_key = request.apiKey.strip()
        normalized_api_secret = request.apiSecret.strip()
        normalized_default_vcn = request.defaultVcn.strip() if request.defaultVcn else "xiaoyan"
        normalized_description = (request.description or "").strip()

        if normalized_name == "":
            raise ValueError("account name cannot be empty")
        if normalized_app_id == "":
            raise ValueError("appId cannot be empty")
        if normalized_api_key == "":
            raise ValueError("apiKey cannot be empty")
        if normalized_api_secret == "":
            raise ValueError("apiSecret cannot be empty")

        with self._lock:
            self._refresh_state_if_needed()
            accounts = self._state.setdefault("accounts", [])
            now_text = datetime.now().isoformat()
            target_account_id = (request.accountId or "").strip() or uuid4().hex[:12]
            existing_account: dict | None = None
            for account in accounts:
                if account["accountId"] == target_account_id:
                    existing_account = account
                    break

            if existing_account is None:
                existing_account = {"accountId": target_account_id}
                accounts.append(existing_account)

            existing_account["name"] = normalized_name
            existing_account["appId"] = normalized_app_id
            existing_account["apiKey"] = normalized_api_key
            existing_account["apiSecret"] = normalized_api_secret
            existing_account["defaultVcn"] = normalized_default_vcn or "xiaoyan"
            existing_account["description"] = normalized_description
            existing_account["enabled"] = bool(request.enabled)
            existing_account["updatedAt"] = now_text

            active_account_id = self._state.get("activeAccountId")
            if active_account_id is None or active_account_id == "":
                self._state["activeAccountId"] = target_account_id
            elif active_account_id == target_account_id and not existing_account["enabled"]:
                self._state["activeAccountId"] = self._find_first_enabled_account_id(accounts)

            if self._state.get("activeAccountId") is None and existing_account["enabled"]:
                self._state["activeAccountId"] = target_account_id

            self._save_state()

            return XfyunTtsAccountView(
                accountId=target_account_id,
                name=normalized_name,
                appId=normalized_app_id,
                apiKey=normalized_api_key,
                apiSecret=normalized_api_secret,
                defaultVcn=normalized_default_vcn or "xiaoyan",
                description=normalized_description,
                enabled=bool(request.enabled),
                isActive=self._state.get("activeAccountId") == target_account_id,
                updatedAt=self._parse_datetime(now_text),
            )

    def set_active_account(self, account_id: str) -> XfyunTtsAccountView:
        normalized_account_id = account_id.strip()
        if normalized_account_id == "":
            raise ValueError("accountId cannot be empty")

        with self._lock:
            self._refresh_state_if_needed()
            for account in self._state.get("accounts", []):
                if account["accountId"] != normalized_account_id:
                    continue
                if not bool(account.get("enabled", True)):
                    raise ValueError("cannot activate a disabled account")

                self._state["activeAccountId"] = normalized_account_id
                self._save_state()
                return XfyunTtsAccountView(
                    accountId=account["accountId"],
                    name=account["name"],
                    appId=account["appId"],
                    apiKey=account["apiKey"],
                    apiSecret=account["apiSecret"],
                    defaultVcn=str(account.get("defaultVcn", "xiaoyan")).strip() or "xiaoyan",
                    description=account.get("description", ""),
                    enabled=bool(account.get("enabled", True)),
                    isActive=True,
                    updatedAt=self._parse_datetime(account.get("updatedAt")),
                )

        raise ValueError("account not found")

    def build_accounts_payload(self) -> dict:
        accounts = self.list_accounts()
        active_account = self.get_active_account()
        return {
            "accounts": [account.model_dump() for account in accounts],
            "activeAccountId": active_account.accountId if active_account is not None else None,
            "activeAccountName": active_account.name if active_account is not None else None,
            "storePath": self._store_path,
        }

    def _load_state(self) -> dict:
        self._ensure_store_directory()
        if not os.path.exists(self._store_path):
            self._last_mtime = None
            return {"activeAccountId": None, "accounts": []}

        try:
            self._last_mtime = os.path.getmtime(self._store_path)
            with open(self._store_path, "r", encoding="utf-8") as file:
                loaded = json.load(file)
        except (OSError, json.JSONDecodeError):
            self._last_mtime = None
            return {"activeAccountId": None, "accounts": []}

        if not isinstance(loaded, dict):
            return {"activeAccountId": None, "accounts": []}

        accounts = loaded.get("accounts")
        if not isinstance(accounts, list):
            accounts = []

        active_account_id = loaded.get("activeAccountId")
        if not isinstance(active_account_id, str):
            active_account_id = None

        return {
            "activeAccountId": active_account_id,
            "accounts": accounts,
        }

    def _save_state(self) -> None:
        self._ensure_store_directory()
        with open(self._store_path, "w", encoding="utf-8") as file:
            json.dump(self._state, file, ensure_ascii=False, indent=2)
        self._last_mtime = os.path.getmtime(self._store_path)

    def _ensure_store_directory(self) -> None:
        os.makedirs(os.path.dirname(self._store_path), exist_ok=True)

    def _refresh_state_if_needed(self) -> None:
        if not os.path.exists(self._store_path):
            if self._last_mtime is not None:
                self._state = {"activeAccountId": None, "accounts": []}
                self._last_mtime = None
            return

        try:
            current_mtime = os.path.getmtime(self._store_path)
        except OSError:
            return

        if self._last_mtime == current_mtime:
            return

        self._state = self._load_state()

    def _find_first_enabled_account_id(self, accounts: list[dict]) -> str | None:
        for account in accounts:
            if bool(account.get("enabled", True)):
                return str(account["accountId"])
        return None

    def _parse_datetime(self, raw_value: str | None) -> datetime:
        if raw_value:
            try:
                return datetime.fromisoformat(raw_value)
            except ValueError:
                pass
        return datetime.now()
