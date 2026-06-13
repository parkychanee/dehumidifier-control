# Dehumidifier Auto Control

LG ThinQ Connect API로 제습기를 자동 제어합니다.
습도 55% 이상이면 켜고, 50% 이하면 끕니다. 15분마다 GitHub Actions로 실행됩니다.

ThinQ API는 물통 가득 찼는지를 상태 조회로 알려주지 않습니다(푸시 알림으로만 옴).
대신 "습도가 여전히 높은데 우리가 끄지 않았음에도 제습기가 꺼져 있다"면 물통이 가득 차서
기기가 스스로 꺼진 것으로 보고, 자동으로 다시 켜지 않습니다. (`state.json`에 이전 상태 기록)

## 설정

GitHub 리포지토리 Settings → Secrets and variables → Actions 에서 아래 3개를 등록하세요.

- `THINQ_PAT`: ThinQ Personal Access Token
- `THINQ_CLIENT_ID`: 임의의 UUID (한 번 생성해서 고정 사용)
- `THINQ_DEVICE_ID`: 제습기 deviceId
