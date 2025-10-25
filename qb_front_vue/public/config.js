window.APP_CONFIG = {
  API_URL: 'http://10.220.150.75:8019/api/v1',
  SUGGESTIONS: [
    {
      id: 'coupon',
      title: '고객 업셀링', // 제목
      text: '업셀링 대상 고객 조회', // 내용
      query: '가입후 경과개월수 3개월 내 티빙 요금제사용 고객 중 티빙계정 활성화 대상', // 버튼 클릭 시 api에 전송되는 텍스트 
      icon: 'star' // 아이콘 타입
    },
    {
      id: 'participants',
      title: '리텐션',
      text: '아이폰 기변 리텐션 캠페인',
      query: '아이폰 13 기변한지 1년이상된 외국인 고객',
      icon: 'users'
    },
    {
      id: 'giftcard',
      title: '결합 상품 유치',
      text: '고가 요금제를 장기 이용하고 있는 고객 조회',
      query: '모바일고객 중 인터넷 미사용 고객 조회해줘',
      icon: 'monitor'
    }
  ]
};