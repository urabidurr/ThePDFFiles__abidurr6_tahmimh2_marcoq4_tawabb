// DOM
const swiper = document.querySelector('#swiper');
const like = document.querySelector('#like');
const dislike = document.querySelector('#dislike');

// variables
let cardCount = 0;

document.querySelectorAll('.card').forEach(cardElement => {
  const existingContent = cardElement.innerHTML;
  const card = new Card({
    onDismiss: appendNewCard,
    onLike: () => {
      like.style.animationPlayState = 'running';
      like.classList.toggle('trigger');
    },
    onDislike: () => {
      dislike.style.animationPlayState = 'running';
      dislike.classList.toggle('trigger');
    }
  });
  card.element.innerHTML = existingContent;
  cardElement.replaceWith(card.element);
  cardCount++;
});

function submitSwipe(direction, username) {
  document.getElementById('swipeDirection').style.color = "red";
  document.getElementById('swipeUser').value = username;
  document.querySelector('form').submit();
}

function appendNewCard() {
  const card = new Card({
    onDismiss: appendNewCard,
    onLike: () => {
      like.style.animationPlayState = 'running';
      like.classList.toggle('trigger');
      let val=document.getElementById("result");
      val.value="accepted";
      console.log("This has been accepted")
    },
    onDislike: () => {
      dislike.style.animationPlayState = 'running';
      dislike.classList.toggle('trigger');
      let val=document.getElementById("result");
      val.value="rejected";
      console.log("This has been rejected")
    }
  });

  const lastCard = document.querySelector('.card:last-child');
  if (lastCard) {
    const content = lastCard.querySelector('.profile-content').cloneNode(true);
    card.element.appendChild(content);
  }

  swiper.append(card.element);
  cardCount++;

  const cards = swiper.querySelectorAll('.card:not(.dismissing)');
  cards.forEach((card, index) => {
    card.style.setProperty('--i', index);
  });
}
