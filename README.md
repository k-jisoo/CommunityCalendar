# CommunityCalendar
## 개발한 기능 및 설명

### 회원 가입 및 로그인 기능 - 권기용

1. 회원가입
    
    회원가입에 필요한 정보 (이메일, ID(닉네임), Password, 이름)을 db에 저장
    

### 게시판 기능 - 김지수

1. 게시글 작성
    
    제목과 내용은 사용자의 입력을 받아 db에 저장.
    
    제목을 입력하지 않을 시 submit 버튼을 클릭해도 넘어가지 않도록 구현.
    
    글쓴이는 세션의 username 정보를 db에 저장.
    
    작성 일과 작성 시간은 시간과 날짜 함수를 사용해 현재 시간과 날짜를 db에 저장.
    
    ![글 쓰기 버튼 클릭 시 팝업](https://prod-files-secure.s3.us-west-2.amazonaws.com/83c75a39-3aba-4ba4-a792-7aefe4b07895/22208d2f-de46-4a2a-9498-a07339717ff0/Untitled.png)
    
    글 쓰기 버튼 클릭 시 팝업
    
    ![글 작성 완료 시 화면](https://prod-files-secure.s3.us-west-2.amazonaws.com/83c75a39-3aba-4ba4-a792-7aefe4b07895/b816fcb7-489c-4c74-a0c4-44e67261c59f/Untitled.png)
    
    글 작성 완료 시 화면
    
2. 게시글 조회
    
    게시글의 제목 클릭 시 제목, 글쓴이, 작성일, 내용을 db에서 불러와 모달에 전달.
    
    글쓴이와 세션의 username이 같다면 수정 및 삭제 버튼 활성화
    
    글쓴이와 세션의 username이 다르다면 수정 및 삭제 버튼 비활성화
    
    ![글쓴이와 세션의 username이 같아 수정과 삭제 버튼이 활성화 된 모습](https://prod-files-secure.s3.us-west-2.amazonaws.com/83c75a39-3aba-4ba4-a792-7aefe4b07895/39e97b1b-543b-407b-b44b-517932382e57/Untitled.png)
    
    글쓴이와 세션의 username이 같아 수정과 삭제 버튼이 활성화 된 모습
    
    ![글쓴이와 세션의 username이 달라 수정과 삭제 버튼이 비활성화 된 모습](https://prod-files-secure.s3.us-west-2.amazonaws.com/83c75a39-3aba-4ba4-a792-7aefe4b07895/e6eab895-b82e-4b52-b1ce-bb0bdb843e74/Untitled.png)
    
    글쓴이와 세션의 username이 달라 수정과 삭제 버튼이 비활성화 된 모습
    
3. 게시글 수정 및 삭제
    
    수정 버튼 클릭 시 기존 제목과 내용을 db에서 불러와 input의 value로 전달.
    
    수정 완료 버튼 클릭 시 db내용 업데이트.
    
    ![게시글 수정 버튼 클릭 시 게시글 수정 모달 팝업](https://prod-files-secure.s3.us-west-2.amazonaws.com/83c75a39-3aba-4ba4-a792-7aefe4b07895/878dfbcd-9fe1-4fde-886c-9fec9a844662/Untitled.png)
    
    게시글 수정 버튼 클릭 시 게시글 수정 모달 팝업
    
    ![수정이 완료되어 제목이 바뀐 모습](https://prod-files-secure.s3.us-west-2.amazonaws.com/83c75a39-3aba-4ba4-a792-7aefe4b07895/082bd8ed-ca1b-4732-9aec-7f99cc6a0567/Untitled.png)
    
    수정이 완료되어 제목이 바뀐 모습
    
4. 페이지네이션
    
    pagenate 함수를 사용해 게시글 10개마다 다음 페이지로 이동하도록 구현.
    
5. 조회수 카운트
    
    제목 클릭 시 그 게시글의 조회수를 1 증가시키고 db에 저장.
    
6. 내가 쓴 글 보기 및 전체 글 보기
    
    내가 쓴 글 보기 버튼 클릭 시 현재 세션의 username과 글쓴이가 같은 게시글을 모두 불러와 조회
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/83c75a39-3aba-4ba4-a792-7aefe4b07895/61409271-fef5-4bb6-b6ef-546587e6e069/Untitled.png)
