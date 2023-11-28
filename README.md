# 자율주행 미니카 시뮬레이션 (ROS2)

"객체지향 모델링" 전공설계 팀 프로젝트 — ROS2와 Gazebo를 이용해 카메라·라이다 센서로 차선을 인식하고 장애물을 회피하며 주행하는 자율주행 미니카 시뮬레이션입니다.

## 1. 프로젝트 배경 및 개요

**기간**: 2023.09 – 2023.11 (약 3개월)
**팀 구성**: 5명
**담당 역할**: 팀장 / 프로젝트 개발 전반, 요건 정리·진행 관리, 회의록·보고서 작성, 발표 준비

Gazebo 시뮬레이션 트랙 위에서 두 대의 차량(`PR001`, `PR002`)이 각각 출발해 차선을 이탈하지 않고 얼마나 먼 구간까지 주행하는지를 평가하는 프로젝트입니다.

## 2. 주요 기능

- **차선 인식 기반 주행** — 카메라 이미지(`/camera1/image_raw`, `/camera3/image_raw`)를 OpenCV(`cv2`, `cv_bridge`)로 처리해 차선을 추적하고 조향 값을 계산
- **장애물 회피** — LiDAR(`/scan`, `LaserScan`)로 전방 장애물을 감지해 정지/회피 로직 수행
- **주행 명령 제어** — `Twist` 메시지로 속도·조향을 `cmd_vel` 토픽에 publish
- **원격 시작 트리거** — 차량 ID별 토픽(`/start_car/{car_id}`)으로 주행 시작 신호를 publish/subscribe

## 3. 노드 구성

| 노드/파일 | 역할 |
|---|---|
| `line_follower.py` / `line_follower2.py` | 카메라 2대 + LiDAR를 이용한 차선 추종 + 장애물 회피 메인 로직 |
| `line_tracker.py` | 이미지에서 차선을 검출하는 알고리즘 |
| `CarStartPublisher.py` | 차량별 주행 시작 신호 publish |
| `CarMoveSubscriber.py` | 주행 명령 subscribe 및 실제 이동 처리 |

## 4. 기술 스택

| 영역 | 기술 |
|---|---|
| 프레임워크 | ROS2 (ament_python 빌드) |
| 언어 | Python (rclpy) |
| 시뮬레이션 | Gazebo (`worlds/car_track.world`) |
| 영상처리 | OpenCV (cv2), cv_bridge |
| 센서 | Camera (Image), LiDAR (LaserScan) |

## 5. 폴더 구조

```
ros2_term_project/       # ROS2 패키지 (노드 구현)
  └ ros2_term_project/   # line_follower, CarStartPublisher 등 실제 노드 코드
ros2_test_follower/      # 테스트용 패키지
launch/                  # 실행 launch 파일 (car_sim.launch.py)
worlds/                  # Gazebo 시뮬레이션 월드 파일
test/                    # 코드 스타일(flake8/pep257)·저작권 테스트
```

## 6. 실행 방법

ROS2(Humble 이상)와 Gazebo가 설치된 환경에서:

```bash
colcon build
source install/setup.bash
ros2 launch ros2_term_project car_sim.launch.py
```
