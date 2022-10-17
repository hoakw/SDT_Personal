# Status Controller

### 개발자 정보
- github ID : hoakw
- Name : 이수준
- email : hoakw@keti.re.kr

### 목적
- 모든 클러스터에 대해서, 자원(CPU, Memory, Network)를 수집하고 DB에 저장
- DB는 mysql을 사용하였으며, Cluster 단위로 자원 크기를 저장
- 수집하는 데이터는 아래와 같음
  * CPU
  * Memory
  * Network Latency (ping cmd 사용)

### build 방법
- GoPATH에 디렉토리를 이동 후,
- build.sh 스크립트 실행
- build.sh에서 docker hub 주소를 직접 입력해야 하므로, 사용자의 ID를 수정해서 실행할 것

### Controller 실행 방법
- start.sh 스크립트 실행

### Controller 삭제 방법
- end.sh 스크립트 실행

### 특이사항
- Network Latency의 경우, ping cmd를 사용하여 데이터를 수집
- ping cmd가 아닌 다른 방법으로 데이터를 수집하도록 설계 내용 수정 필요
- Network에 관해서, 클러스터 내의 Pod들의 복잡도를 활용하는 것을 추진 계획
