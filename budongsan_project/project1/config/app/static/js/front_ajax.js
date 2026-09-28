// 예측 가격, 추천 매물, 통계 정보

window.onload = function(){
  //js fetch
	document.querySelector("#submitButton").onclick = function(){
    const data = {
      gu: $('#gu').val(),
      dong: $('#dong').val(),
      width: $('#width').val(),
      subway: $('#subway').val(),
      river: $('#river').val(),
      // csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
    };
  
		const url = 'predict';
		fetch(url).then(res => {
			if(res.status === 200){
				return res.json();
			}else{
				console.log(`HTTP error! status:${res.status}`);
			}
		}).then(jsonData =>{
			renderRecommendedProperties(jsonData);
		}).catch(err => {
			console.log(err);
		})
	}
}


//////////////////////////////////
function loadNewPage() {
  const data = {
    gu: $('#gu').val(),
    dong: $('#dong').val(),
    width: $('#width').val(),
    subway: $('#subway').val(),
    river: $('#river').val(),
    // csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
  };

  $.ajax({ // 예상 가격
    url: "{% url 'predict' %}",
    method: "GET",
    data: data,
    success: function(response) {
      // console.log(response)
      // 요청이 성공하면 응답을 갖는 response 객체를 받음
      // 첨부된 코드와 호환되도록 응답 데이터에서 예상가격 추출, 예상할 경우 변환 필요
      // const predictedPrice = JSON.stringify(response);

      // 예상가격 출력
      $('#predict_price').html(response.gu + " 원");
    },
  });

  $.ajax({ // 추천 매물
      url: "{% url 'recommand' %}", // 추천 매물을 가져올 URL
      method: "GET",
      data: data, // 조회 조건 데이터
      success: function(response) {
          renderRecommendedProperties(response);
      }
  });

  $.ajax({ // 통계 정보
    url: "{% url 'chart' %}",
    method: "GET",
    success: function (response) {
      $("#chart").html(response);
      initializeCharts(); // 통계 차트 초기화 함수 호출
    },
  });
}

function renderRecommendedProperties(properties) {
  let listItemsHTML = '';

  properties.forEach(property => {
      listItemsHTML += `
          <a href="#" class="list-group-item list-group-item-action">
              <div class="d-flex w-100 justify-content-between">
                  <h5 class="mb-1">${property.title}</h5>
                  <small class="text-body-secondary">${property.price}</small>
              </div>
              <p class="mb-1">${property.desc}</p>
              <small class="text-body-secondary">${property.location}</small>
          </a>
      `;
  });

  document.querySelector('#recom_list').innerHTML = listItemsHTML;
}

// // 조회 버튼 클릭시 loadNewPage 함수 실행
$("#submitButton").click(loadNewPage);