$('.visual').slick({
  autoplay: true,
  autoplaySpeed: 3000,
  dots: true,
});

$(document).on('ready', function() {
  $('.slider_thumb').slick({
      arrows:false, // スライドの左右の矢印ボタン
      asNavFor:'.thumb' // スライダを他のスライダのナビゲーションに設定する（class名またはID名）
  });
  $('.thumb').slick({
      asNavFor:'.slider_thumb', // スライダを他のスライダのナビゲーションに設定する（class名またはID名）
      focusOnSelect: true, // クリックでのスライド切り替えを有効にするか
      slidesToShow:4, // 表示するスライド数を設定
      slidesToScroll:1 // スクロールするスライド数を設定
  });  
});