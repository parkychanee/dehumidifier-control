# Dehumidifier Auto Control

LG ThinQ Connect API로 제습기를 자동 제어합니다.
습도 55% 이상이면 켜고, 50% 이하면 끕니다. 15분마다 GitHub Actions로 실행됩니다.

## 설정

GitHub 리포지토리 Settings → Secrets and variables → Actions 에서 아래 3개를 등록하세요.

- `THINQ_PAT`: ThinQ Personal Access Token
- `THINQ_CLIENT_ID`: 임의의 UUID (한 번 생성해서 고정 사용)
- `THINQ_DEVICE_ID`: 제습기 deviceId
