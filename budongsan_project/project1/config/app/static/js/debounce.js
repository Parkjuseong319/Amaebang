// debounce 함수 정의: 중복 요청 제거를 위해, 주어진 함수의 연속 실행을 제한하며, 제한된 시간이 경과한 후에만 주어진 함수를 실행
function debounce(func, wait) {
  let timeout;
  return function () {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, arguments), wait);
  };
}

// 웹 페이지의 select 태그와 submitButton 요소 선택
const selectBoxes = document.querySelectorAll('select');
const submitButton = document.getElementById('submitButton');

// 모든 select 태그가 선택된 경우에만 submitButton 활성화하는 함수
function updateSubmitButtonState() {
  const areAllSelected = Array.from(selectBoxes).every(selectBox => selectBox.value);
  submitButton.disabled = !areAllSelected;
}

// 선택상자 변경이 감지될 때마다 상태 업데이트하고 이벤트를 출력하는 함수
function onBoxChange(event) {
  console.log(`${event.target.id} 값이 선택되었습니다: ${event.target.value}`);
  debounceUpdateSubmitButtonState();
}

// updateSubmitButtonState 함수에 대한 debounce 적용
const debounceUpdateSubmitButtonState = debounce(updateSubmitButtonState, 300);

// 선택 상자에 이벤트 리스너 추가
selectBoxes.forEach(selectBox => {
  selectBox.addEventListener("change", onBoxChange);
});

// 초기 페이지 로드 시 버튼 상태 확인
updateSubmitButtonState(); 
