const changeGrid = () => {
  const mainAdept = () => {
    // получаем элементы из документа

    let main = document.querySelector("#main");
    let grid = document.getElementById("grid-section");
    let aside = document.querySelector(".aside-right");

    // тэги а hot discussion & hot watched
    let hd = document.querySelector(".link-hot-disscused");
    let hw = document.querySelector(".link-hot-watched");
    // jpgs
    let jpgsAside = document.querySelectorAll(".aside-right .news-img");
    let jpgsMain = document.querySelectorAll(".grid .news-img");
    // ширина текущего экрана
    let mainWidth = main.offsetWidth;

    // получаем их css свойства из окна
    let jpgMainCurH = window.getComputedStyle(jpgsMain[0]).height;

    for (jpg of jpgsAside) {
      jpg.style.height = jpgMainCurH;
    }

    // aside.style.height = jpgMainCurH;
    // console.log(`aside: ${aside.style.width} картинка ${jpgMainCurWid}`);

    if (Number(mainWidth) <= 1100) {
      grid.classList.add("grid2");
      grid.classList.remove("grid3");
      hd.style.fontSize = "8px";
      hw.style.fontSize = "8px";
      aside.style.width = "33%";
    } else {
      grid.classList.add("grid3");
      grid.classList.remove("grid2");
      hd.style.fontSize = "10px";
      hw.style.fontSize = "10px";
      aside.style.width = "25%";
    }
  };
  window.addEventListener("resize", mainAdept);
  window.addEventListener("load", mainAdept);
};

const headerNavGameLinks = () => {
  let navList = document.querySelectorAll(".game-icons-list li");
  for (let li of navList) {
    let img = li.children[0];
    let a = li.children[1];
    img.addEventListener("mouseenter", () => {
      a.classList.toggle("game-activ");
    });
    img.addEventListener("mouseleave", () => {
      a.classList.toggle("game-activ");
    });
  }
};

const footerContactLinks = () => {
  let footerNavList = document.querySelectorAll(".contacts-footer li");
  for (let li of footerNavList) {
    let a = li.children[0];
    let img = a.children[0];
    a.addEventListener("mouseenter", () => {
      a.style.textDecoration = "underline";
      img.classList.toggle("footer-icon-contacts");
      img.classList.toggle("footer-icon-contacts-activ");
    });
    a.addEventListener("mouseleave", () => {
      a.style.textDecoration = "none";
      img.classList.toggle("footer-icon-contacts-activ");
      img.classList.toggle("footer-icon-contacts");
    });
  }
};

const logoImgRotate = () => {
  let a = document.querySelector(".home");
  let img = a.children[0];
  a.addEventListener("mouseenter", () => {
    img.classList.toggle("icon-logo-activ");
  });
  a.addEventListener("mouseleave", () => {
    img.classList.toggle("icon-logo-activ");
  });
};

const navMenuOpen = () => {
  let btn = document.querySelector(".btn-header-nav");
  let div = document.querySelector(".header-right");
  let nav = document.querySelector(".nav-menu-list");
  let exit = document.querySelector(
    ".nav-open .nav-menu-icons[name='close-outline']"
  );

  const classToggle = () => {
    btn.classList.add("btn-nav-border");
    div.classList.remove("nav-open");
  };

  const toggleNavOpen = (evt) => {
    if (!exit) {
      btn.classList.remove("btn-nav-border");
      div.classList.add("nav-open");
      document.body.addEventListener("click", function (evt) {
        if (evt.target !== nav && evt.target !== btn) {
          classToggle();
        }
      });
    } else {
      classToggle();
    }
  };

  btn.addEventListener("mousedown", toggleNavOpen);
};

const navBarRawsSelection = () => {
  let ul = document.querySelectorAll(".nav-menu-list li");
  for (let li of ul) {
    li.addEventListener("mouseenter", () => {
      li.style.background = "#222";
    });
    li.addEventListener("mouseleave", () => {
      li.style.background = "hsla(0, 0%, 8%, 0.925)";
    });
  }
};

const safaryAdeptLink = () => {
  const allLinks = document.querySelectorAll("a:link");
  allLinks.forEach(function (link) {
    link.addEventListener("click", function (e) {
      const href = link.getAttribute("href");
      //scroll back to the top
      if (href.startsWith("#")) {
        e.preventDefault();
        if (href === "#") {
          window.scrollTo({
            top: 0,
            behavior: "smooth",
          });
        }
        //scroll to other links
        else if (href !== "#") {
          e.preventDefault();
          const sectionEl = document.querySelector(href);
          console.log(sectionEl);
          sectionEl.scrollIntoView({ behavior: "smooth" });
        }
      }
    });
  });
};

headerNavGameLinks();
footerContactLinks();
logoImgRotate();
navMenuOpen();
navBarRawsSelection();
safaryAdeptLink();
