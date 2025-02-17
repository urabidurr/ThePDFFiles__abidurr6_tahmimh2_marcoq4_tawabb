class Card {
    constructor({
      onDismiss,
      onLike,
      onDislike
    }) {
      this.onDismiss = onDismiss;
      this.onLike = onLike;
      this.onDislike = onDislike;
      this.#init();
    }
  

    #startPoint;
    #offsetX;
    #offsetY;
  
    #isTouchDevice = () => {
      return (('ontouchstart' in window) ||
        (navigator.maxTouchPoints > 0) ||
        (navigator.msMaxTouchPoints > 0));
    }
  
    #init = () => {
      const card = document.createElement('div');
      card.classList.add('card');
      this.element = card;
      if (this.#isTouchDevice()) {
        this.#listenToTouchEvents();
      } else {
        this.#listenToMouseEvents();
      }
    }
  
    #listenToTouchEvents = () => {
      this.element.addEventListener('touchstart', (e) => {
        const touch = e.changedTouches[0];
        if (!touch) return;
        const { clientX, clientY } = touch;
        this.#startPoint = { x: clientX, y: clientY }
        document.addEventListener('touchmove', this.#handleTouchMove);
        this.element.style.transition = 'transform 0s';
      });
  
      document.addEventListener('touchend', this.#handleTouchEnd);
      document.addEventListener('cancel', this.#handleTouchEnd);
    }
  
    #listenToMouseEvents = () => {
      this.element.addEventListener('mousedown', (e) => {
        const { clientX, clientY } = e;
        this.#startPoint = { x: clientX, y: clientY }
        document.addEventListener('mousemove', this.#handleMouseMove);
        this.element.style.transition = 'transform 0s';
      });
  
      document.addEventListener('mouseup', this.#handleMoveUp);
  
      
    }
  
    #handleMove = (x, y) => {
      this.#offsetX = x - this.#startPoint.x;
      this.#offsetY = y - this.#startPoint.y;
      const rotate = this.#offsetX * 0.1;
      this.element.style.transform = `translate(${this.#offsetX}px, ${this.#offsetY}px) rotate(${rotate}deg)`;
      // dismiss card
      if (Math.abs(this.#offsetX) > this.element.clientWidth * 0.7) {
        this.#dismiss(this.#offsetX > 0 ? 1 : -1);
      }
    }
  
    // mouse event handlers
    #handleMouseMove = (e) => {
      e.preventDefault();
      if (!this.#startPoint) return;
      const { clientX, clientY } = e;
      this.#handleMove(clientX, clientY);
    }
  
    #handleMoveUp = () => {
      this.#startPoint = null;
      document.removeEventListener('mousemove', this.#handleMouseMove);
      this.element.style.transform = '';
    }
  
    // touch event handlers
    #handleTouchMove = (e) => {
      if (!this.#startPoint) return;
      const touch = e.changedTouches[0];
      if (!touch) return;
      const { clientX, clientY } = touch;
      this.#handleMove(clientX, clientY);
    }
  
    #handleTouchEnd = () => {
      this.#startPoint = null;
      document.removeEventListener('touchmove', this.#handleTouchMove);
      this.element.style.transform = '';
    }
  
    #dismiss = (direction) => {
      this.#startPoint = null;
      document.removeEventListener('mouseup', this.#handleMoveUp);
      document.removeEventListener('mousemove', this.#handleMouseMove);
      document.removeEventListener('touchend', this.#handleTouchEnd);
      document.removeEventListener('touchmove', this.#handleTouchMove);
      const username = this.element.getAttribute('data-username');
      fetch('/match', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `swipe_direction=${direction > 0 ? 'like' : 'dislike'}&swiped_user=${username}`
      });
      const formData = new FormData();
      formData.append('swipe_direction', direction > 0 ? 'like' : 'dislike');
      formData.append('swiped_user', username);
      
      fetch('/match', {
        method: 'POST',
        body: formData
      }).then(response => {
        console.log('Swipe sent:', direction > 0 ? 'like' : 'dislike', username);
      }).catch(error => {
        console.error('Error:', error);
      });

      this.element.style.transition = 'transform 1s';
      this.element.style.transform = `translate(${direction * window.innerWidth}px, ${this.#offsetY}px) rotate(${90 * direction}deg)`;
      this.element.classList.add('dismissing');
      setTimeout(() => {
        this.element.remove();
      }, 1000);
      if (typeof this.onDismiss === 'function') {
        this.onDismiss();
      }
      if (typeof this.onLike === 'function' && direction === 1) {
        this.onLike();
      }
      if (typeof this.onDislike === 'function' && direction === -1) {
        this.onDislike();
      }
    }
  }
