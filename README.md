# metaheuristic
메타휴리스틱을 이용한 코드 정리

findbignumber_ga.py
-이진수의 최댓값을 GA로 찾는 문제

findbignumber_LGA.py
-GA의 새로운 방법론 개발
-특정 시점마다 모든 유전자에 변이연산을 시행

pso.py
-Particlle swam optimaization을 직접 구현해보고자 만듬 -일정 바운더리 내에서 랜덤하게 해를 생성하고 0,0이 최적해인 함수에서 잘 수렴하는지를 확인해봄

scheduling_GA-SHIN.py
-SingleMachineProblem을 GA로 해결해보기 위해 만듬 -직접 균일분포로 job의 processing time과 due date를 만들고 만들어진 데이터에서 total tardiness를 최소화 시키거나 total flowtime을 최소화 시키는 목적함수를 가지고 최적해를 찾음

scheduling.csv
-스케줄링 문제의 데이터 파일
