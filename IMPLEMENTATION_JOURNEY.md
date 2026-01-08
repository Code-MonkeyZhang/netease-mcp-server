# NetEase Music MCP Implementation Journey

## 1. Project Background
**Objective**: Enable the AI Agent to control the NetEase Cloud Music (macOS) desktop application, access user data (playlists, recommendations), and playback control.

**Initial State**:
- Existing solution: `CloudMusic_Auto_Player` (Legacy).
- Mechanism: Selenium-based UI automation + PyAutoGUI hotkeys.
- Issues: Slow, unstable (fragile XPath), required `chromedriver` maintenance, "Daily Recommend" often failed due to page load timing.

## 2. Technical Decisions

### 2.1 The Pivot to Open API
We decided to move away from UI automation to a data-driven approach using the **NetEase Cloud Music Open API**.
- **Library**: `pyncm` (Python NetEase Cloud Music).
- **Benefits**:
    - **Stability**: API endpoints are more stable than UI DOM structures.
    - **Speed**: Fetching JSON is milliseconds; loading a webview is seconds.
    - **Features**: Direct access to user's "Red Heart" list and Daily Recommendations without parsing HTML.

### 2.2 Authentication Strategy
- **Challenge**: Standard OAuth 2.0 (H5 wake-up) requires an approved Developer App ID, which is unavailable for local scripts.
- **Solution**: **QR Code Login** (simulating the official client/web behavior).
    - Request a UUID -> Generate QR Code -> User scans via App -> Polling for status -> Save Cookies.
- **Persistence**: Saved session cookies to `src/storage/cookies.json` for long-term access.

### 2.3 Playback Control Mechanism
- **Challenge**: The Open API provides song URLs/IDs, but we need to play them in the *Desktop App*, not a headless Python player.
- **Solution**: **macOS URL Scheme (`orpheus://`)**.
    - Command: `subprocess.run(["open", "orpheus://..."])`.
    - **Critical Finding**: Simply opening `orpheus://song/ID` only *shows* the song. To *auto-play*, we must use a **Base64 encoded JSON command**.
    - **Format**: `{"type": "song", "id": "...", "cmd": "play"}` -> Base64 -> `orpheus://BASE64_STRING`.

## 3. Implementation Hurdles & Fixes

### 3.1 Import Errors
- **Issue**: `ImportError: attempted relative import...` when running scripts directly.
- **Fix**: Used absolute imports or managed `PYTHONPATH` correctly in `settings.json`.

### 3.2 Session Persistence Failure
- **Issue**: `pyncm.DumpSessionAsString` / `LoadSessionFromString` (Pickle-based) failed to restore cookies correctly across sessions.
- **Fix**: Switched to manually dumping `cookies.get_dict()` to a plain `cookies.json` file and restoring via `session.cookies.update()`.

### 3.3 API Signature Confusion
- **Issue**: `WeapiCryptoRequest() takes 1 positional argument but 2 were given`.
- **Cause**: `pyncm`'s `WeapiCryptoRequest` is a decorator factory in some contexts or requires specific usage.
- **Fix**: Wrapped the API call in an inner function decorated with `@apis.WeapiCryptoRequest`.

### 3.4 Playback Silence (The "Cold Start" Issue)
- **Issue**: The URL Scheme command was sent, the app opened, but music didn't start.
- **Verification**: Verified URL generation was identical to the working legacy script.
- **Root Cause**: Likely app "Cold Start" latency or environment differences.
- **Resolution**: Ensured correct Base64 encoding of the JSON command `{"cmd": "play"}`.

### 3.5 Environment Management
- **Issue**: Potential conflicts with system Python / Anaconda.
- **Fix**: Migrated to a strictly isolated virtual environment managed by **`uv`**.
    - Configured `settings.json` to use `uv run` for deterministic execution.

## 4. Final Architecture
- **Language**: Python 3.11+
- **Core Libs**: `fastmcp`, `pyncm`, `qrcode`.
- **Env**: `uv` managed `.venv`.
- **Entry**: `src/main.py` (FastMCP Server).
