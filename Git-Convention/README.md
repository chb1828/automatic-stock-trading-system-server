### 아래의 깃 컨벤션을 따릅니다.

---

# Git-Convention-Guide

작성자: @chb

---

본 문서는 "ASTS" 서비스를 개발위해 사용 사용될 Git사용을 위한 가이드라인을 제공합니다.

---

---

# 1. Branching strategy

---

## 1. Main Branches

### 1. `main`

- `origin/main`는 항상 최신 소스를 반영하는 branch
- 개발자는 항상 `main` branch를 branching 하거나 merge.


## 2. Supporting Branches

### 1. `feature`

- `origin/feature-<tbd number>` 는 새로운 feature를 개발 할 때 사용.
- Must branch from: `master`
- Must merge back into: `master`
- Branch naming convention: `feature-<tbd number>`
- `<tbd number>` represents the Basecamp project to which Project Management will be tracked.

```
# Make new feature branch
$ git checkout -b feature-id master                 // creates a local branch for the new feature
$ git push origin feature-id                        // makes the new feature remotely available

# Periodically, merge into your feature branch
$ git merge master                                  // merges changes from master into feature branch

# When development on the feature is complete
$ git checkout master                               // change to the master branch  
$ git merge --no-ff feature-id                      // makes sure to create a commit object during merge
$ git push origin master                            // push merge changes
$ git push origin :feature-id                       // deletes the remote branch
```

### 2. `bug`

- `origin/bug-<tbd number>` 는 수정되어야 할 버그 발견시, 버그 수정을 위해 사용.
- `bug` branch는 일반적으로 배포 주기 내에 포함되어 `master`에 merge 되어야 한다..
- Must branch from: `master`
- Must merge back into: `master`
- Branch naming convention: `bug-<tbd number>`

```
# Make new bug branch
$ git checkout -b bug-id master                     // creates a local branch for the new bug
$ git push origin bug-id                            // makes the new bug remotely available

# Periodically, merge into your feature branch
$ git merge master                                  // merges changes from master into feature branch

# When development on the bug is complete
$ git checkout master                               // change to the master branch  
$ git merge --no-ff bug-id                          // makes sure to create a commit object during merge
$ git push origin master                            // push merge changes
$ git push origin :bug-id                           // deletes the remote branch
```


### 3. Workflow Diagram

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/c42699cf-fe19-4448-bee7-f5ca0bcd1af9/Untitled.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/c42699cf-fe19-4448-bee7-f5ca0bcd1af9/Untitled.png)

# 2. Commit message (이 부분은 불편하면 삭제하겠습니다. 다만 다른 사람이 쉽게 알아 볼 수 있도록 작성해 주십시오)

---

### Commit message template

- Commit message는 기본적으로 아래의 Template를 따라 작성한다.
- 제목(`<type>:<title>`)은 *반드시* 입력하고, 최대 40글자 까지 영문 명령조로 작성
- 본문(`<description>`)은 어떻게 보다는 무엇을, 왜 변경 했는지를 작성(선택)
- 이슈넘버(`<issue-number>`)는 연관된 이슈를 기재하며, 여러 개 추가 가능하다.(선택)

```
Feat: Implement user model class 

<description>
로그인 기능 구현을 위해, User 모델 작성. 

<issue-number>
#512
```

### How to apply template file

- Commit message template file과 해당 템플릿 파일을 적용하는 방법
1. `.git-commit-template.txt` 작성

/your/project/root/path/.**git-commit-template.txt**

```
<type>: <title> 
# <type
# - feat   : 새로운 기능 추가
# - fix    : 버그 수정 
# - docs   : 문서 수정
# - style  : 코드 포맷팅, 세미콜론 누락, 코드 변경이 없는 경우
# - refact : 코드 리펙토링
# - test   : 테스트 코드, 리펙토링 테스트 코드 추가
# - chore  : 빌드 업무 수정, 패키지 매니저 수정

# <title>
# 제목의 길이는 최대 40글자까지 한글로 간단 명료하게 작성 
# <type>: 한칸 띄고 <title 작성>
# 제목을 작성하고 반드시 빈 줄 한 줄을 만들어야 함 
# 제목에 .(마침표) 금지 

<description> 
# 내용의 길이는 한 줄당 60글자 내외에서 줄 바꿈. 한글로 간단 명료하게 작성 
# 어떻게 보다는 무엇을, 왜 변경했는지를 작성할 것 (필수) 

<issue-number> 
# 연관된 이슈 첨부, 여러 개 추가 가능2. 프로젝트에 commit template 적용
```

2. `commit.template` 등록

```bash
# On your project root
$ git config --global commit.template ./.git-commit-template.txt
```
