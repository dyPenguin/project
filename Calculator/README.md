#  Calculator — 계산기

The calculator application implemented in Python using PyQt5. The Ui was designed in Qt Designer.

<a href="https://www.python.org">
<img src="https://img.shields.io/badge/Python3+-3776AB?style=flat&logo=PYTHON&logoColor=white&link=https://www.python.org/"></a>
<a href="https://www.anaconda.com">
<img src="https://img.shields.io/badge/Anaconda-44A833?style=flat&logo=Anaconda&logoColor=white&link=https://www.anaconda.com/"></a>
<a href="https://qt-brandbook.webflow.io">
<img src="https://img.shields.io/badge/Qt-41CD52?style=flat&logo=Qt&logoColor=white&link=https://qt-brandbook.webflow.io/"></a>

#### [실행 파일(.exe) 다운](https://vo.la/qMtA3)


## UI Design
<img src="https://user-images.githubusercontent.com/69224744/150070708-9cdbc6f3-01f8-434d-9696-82ae390e707c.gif" title="실행 결과" hspace="10"/>


## Windows based:
### Prerequisite
- PyQt5
- Qt Designer (Only for developers for editing layouts)

## Feature
- 입력한 수식을 화면에 출력
- 입력 가능 숫자의 자리수를 제한 (소수점 포함 11자리)
- 연산자 입력 시, Backspace 기능 제한
- 예외 처리 시, 일부 버튼을 비활성화 (ex. 0으로 나눈 경우)
  - 활성화 된 버튼을 누르면 초기 상태로 복구

- 실수 연산 시 .0으로 끝나면 정수로 출력

<img src="https://user-images.githubusercontent.com/69224744/150540730-2cdf3f25-3379-4c1d-8524-361e4c62ea7c.gif" hspace="10"/>

## 개선 사항
- 부동 소수점 입력 시, 지수 형태로 출력
- 음수 입력 기능 필요
- 자리수 구분 , 필요 → 구현 완료 (+22.01.14)



