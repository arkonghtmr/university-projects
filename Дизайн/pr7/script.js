const data = {
  audience: [
    {
      icon: "user",
      title: "Новички без опыта",
      description:
        "Вы хотите освоить творческую профессию с нуля и работать удаленно. Мы научим вас всему с самых основ.",
    },
    {
      icon: "briefcase",
      title: "Смена профессии",
      description:
        "Работаете в сфере с низкой оплатой и хотите перейти в IT. Моушн-дизайн - ваш шанс на новый карьерный путь.",
    },
    {
      icon: "palette",
      title: "Графические дизайнеры",
      description:
        "Уже занимаетесь дизайном и хотите расширить навыки в анимацию. Добавьте в портфолио востребованный скилл.",
    },
  ],
  benefits: [
    {
      icon: "briefcase",
      title: "Готовое портфолио",
      description: "Шоурил из 5 профессиональных анимационных работ для демонстрации заказчикам.",
    },
    {
      icon: "code",
      title: "Владение софтом",
      description: "Полное освоение After Effects и Cinema 4D - главных инструментов моушн-дизайнера.",
    },
    {
      icon: "award",
      title: "Сертификат",
      description: "Официальный документ о прохождении курса для вашего резюме.",
    },
    {
      icon: "users",
      title: "Помощь в поиске заказов",
      description: "Консультации по созданию профиля на биржах и привлечению первых клиентов.",
    },
  ],
  program: [
    {
      week: "Неделя 1-2",
      title: "Основы анимации и After Effects",
      lessons: [
        "Введение в моушн-дизайн: история, примеры, сферы применения",
        "Интерфейс After Effects: панели, композиции, слои",
        "12 принципов анимации Диснея",
        "Ключевые кадры и работа с таймлайном",
        "Анимация формы и трансформации",
        "Проект: создание простой анимированной инфографики",
      ],
    },
    {
      week: "Неделя 3-4",
      title: "Продвинутые техники в After Effects",
      lessons: [
        "Работа с масками и матами",
        "Эффекты и пресеты: правильное применение",
        "Анимация текста: preset animator и вручную",
        "Родительские связи (parenting) и null-объекты",
        "Выражения (expressions) для автоматизации",
        "Проект: анимированный типографический постер",
      ],
    },
    {
      week: "Неделя 5-6",
      title: "Основы 3D-анимации в Cinema 4D",
      lessons: [
        "Интерфейс Cinema 4D: навигация, примитивы, деформеры",
        "Моделирование простых объектов",
        "Материалы и текстуры: настройка и применение",
        "Освещение трёхточечной схемой",
        "Камеры и композиция кадра",
        "Проект: анимация 3D-логотипа",
      ],
    },
    {
      week: "Неделя 7-8",
      title: "Финальные проекты и шоурил",
      lessons: [
        "Создание сложной сцены с персонажем",
        "Работа со звуком и синхронизация с анимацией",
        "Цветокоррекция и финальный рендер",
        "Экспорт для разных платформ (Instagram, YouTube, Behance)",
        "Сборка шоурила из всех проектов",
        "Защита финального проекта перед наставником",
      ],
    },
  ],
  works: [
    { title: "Заставка для музыкального фестиваля", author: "Анна К.", image: "assets/work-01.jpg" },
    { title: "3D-ролик для бренда кроссовок", author: "Дмитрий М.", image: "assets/work-02.jpg" },
    { title: "Кинетическая типографика для подкаста", author: "Елена С.", image: "assets/work-03.jpg" },
    { title: "Анимация интерфейса фитнес-приложения", author: "Михаил В.", image: "assets/work-04.jpg" },
    { title: "Рекламный шоурил кофейни", author: "Ольга П.", image: "assets/work-05.jpg" },
    { title: "Инфографика для финансового сервиса", author: "Сергей Л.", image: "assets/work-06.jpg" },
    { title: "Logo reveal для студии интерьера", author: "Мария Н.", image: "assets/work-07.jpg" },
    { title: "Промо-анимация онлайн-курса", author: "Илья Р.", image: "assets/work-08.jpg" },
    { title: "Персонажная сцена для YouTube-канала", author: "Вера Т.", image: "assets/work-09.jpg" },
  ],
  teachers: [
    {
      name: "Александр Соколов",
      position: "Арт-директор в Яндекс",
      experience: "12 лет в индустрии",
      achievements: "Работал над рекламными кампаниями для Samsung, Adidas, Red Bull",
      colors: ["#8b5cf6", "#5b21b6"],
    },
    {
      name: "Мария Петрова",
      position: "Lead Motion Designer в VK",
      experience: "8 лет в моушн-дизайне",
      achievements: "Создала анимацию для топовых стриминговых платформ",
      colors: ["#ec4899", "#9d174d"],
    },
    {
      name: "Дмитрий Волков",
      position: "Freelance Motion Designer",
      experience: "10 лет опыта",
      achievements: "Более 200 завершённых проектов, топ-1% на Upwork",
      colors: ["#38bdf8", "#1d4ed8"],
    },
  ],
  pricing: [
    {
      name: "Стандарт",
      price: "29 900",
      popular: false,
      features: [
        "Доступ ко всем урокам курса",
        "Проверка домашних заданий",
        "Чат с однокурсниками",
        "Сертификат о прохождении",
        "Доступ к материалам 6 месяцев",
      ],
    },
    {
      name: "С наставником",
      price: "49 900",
      popular: true,
      features: [
        "Всё из тарифа \"Стандарт\"",
        "Личный наставник на весь курс",
        "Еженедельные созвоны 1-на-1",
        "Детальный разбор каждой работы",
        "Помощь в создании портфолио",
        "Консультация по трудоустройству",
        "Доступ к материалам навсегда",
      ],
    },
  ],
  career: [
    {
      icon: "file",
      title: "Резюме и портфолио",
      description: "Поможем составить продающее резюме и оформить ваши работы на Behance.",
    },
    {
      icon: "users",
      title: "Регистрация на биржах",
      description: "Создадим профили на Upwork, Freelancer и русскоязычных платформах.",
    },
    {
      icon: "trend",
      title: "Стратегия продвижения",
      description: "Расскажем, как находить первых клиентов и правильно оценивать работу.",
    },
    {
      icon: "handshake",
      title: "Поддержка после курса",
      description: "Консультации в закрытом чате выпускников и разбор сложных кейсов.",
    },
  ],
  faq: [
    {
      question: "Нужно ли уметь рисовать, чтобы стать моушн-дизайнером?",
      answer:
        "Нет, художественные навыки не обязательны. Моушн-дизайн - это работа с готовыми объектами, формами и типографикой. Главное - чувство композиции и ритма, которые мы развиваем на курсе.",
    },
    {
      question: "Какой компьютер нужен для обучения?",
      answer:
        "Минимальные требования: процессор Intel i5 или аналог, 8 ГБ RAM, видеокарта с 2 ГБ памяти. Для комфортной работы рекомендуем 16 ГБ RAM. Подойдут как Windows, так и macOS.",
    },
    {
      question: "Сколько времени нужно уделять учёбе?",
      answer:
        "Рекомендуем 10-15 часов в неделю: просмотр уроков (3-4 часа) и выполнение практических заданий (7-11 часов). График гибкий - можно учиться в удобное время.",
    },
    {
      question: "Что если я не успею сдать проект вовремя?",
      answer:
        "Ничего страшного! Мы понимаем, что у всех разный темп. Доступ к материалам остаётся на 6 месяцев (навсегда в тарифе \"С наставником\"), так что вы сможете завершить всё в комфортном режиме.",
    },
    {
      question: "Можно ли получить возврат, если курс не подойдёт?",
      answer:
        "Да, в течение первых 7 дней с момента старта курса мы вернём 100% оплаты без лишних вопросов, если вы поймёте, что обучение вам не подходит.",
    },
    {
      question: "Помогаете ли с поиском работы после курса?",
      answer:
        "Да! Мы помогаем составить резюме, оформить портфолио на Behance, зарегистрироваться на биржах фриланса и консультируем по ценообразованию. У нас также есть закрытый чат выпускников для обмена опытом.",
    },
  ],
};

const iconPaths = {
  user: '<path d="M20 21a8 8 0 0 0-16 0"/><circle cx="12" cy="7" r="4"/>',
  briefcase: '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><path d="M3 12h18"/>',
  palette: '<path d="M12 22a10 10 0 1 1 10-10c0 1.8-1.5 3-3.2 3H17a2 2 0 0 0-2 2v1.1c0 2.1-1.3 3.9-3 3.9Z"/><circle cx="7.5" cy="10.5" r="1"/><circle cx="12" cy="7.5" r="1"/><circle cx="16.5" cy="10.5" r="1"/>',
  code: '<path d="m8 9-4 3 4 3"/><path d="m16 9 4 3-4 3"/><path d="m14 5-4 14"/>',
  award: '<circle cx="12" cy="8" r="5"/><path d="m8.5 12.5-1.5 8 5-3 5 3-1.5-8"/>',
  users: '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9"/><path d="M16 3.1a4 4 0 0 1 0 7.8"/>',
  file: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6"/><path d="M8 13h8"/><path d="M8 17h5"/>',
  trend: '<path d="m3 17 6-6 4 4 8-8"/><path d="M14 7h7v7"/>',
  handshake: '<path d="m11 17 2 2a3 3 0 0 0 4 0l4-4"/><path d="m5 12 5-5 4 4"/><path d="m2 14 3-3 5 5"/><path d="m18 11 2 2"/>',
  star: '<path d="m12 2 2.9 6 6.6.9-4.8 4.7 1.1 6.5-5.8-3.1-5.8 3.1 1.1-6.5-4.8-4.7 6.6-.9Z"/>',
};

function icon(name) {
  return `<svg viewBox="0 0 24 24" aria-hidden="true">${iconPaths[name] || iconPaths.star}</svg>`;
}

function initials(name) {
  return name
    .split(" ")
    .map((part) => part[0])
    .join("");
}

function renderCards() {
  const audience = document.querySelector('[data-render="audience"]');
  audience.innerHTML = data.audience
    .map(
      (item) => `
        <article class="card">
          <span class="icon-box">${icon(item.icon)}</span>
          <h3>${item.title}</h3>
          <p>${item.description}</p>
        </article>
      `,
    )
    .join("");

  const benefits = document.querySelector('[data-render="benefits"]');
  benefits.innerHTML = data.benefits
    .map(
      (item) => `
        <article class="benefit-card">
          <div class="benefit-inner">
            <span class="icon-box">${icon(item.icon)}</span>
            <div>
              <h3>${item.title}</h3>
              <p>${item.description}</p>
            </div>
          </div>
        </article>
      `,
    )
    .join("");

  const works = document.querySelector('[data-render="works"]');
  works.innerHTML = data.works
    .map(
      (item) => `
        <article class="work-card">
          <img src="${item.image}" alt="${item.title}" loading="lazy">
          <span class="work-play"><span></span></span>
          <div class="work-caption">
            <strong>${item.title}</strong>
            <span>${item.author}</span>
          </div>
        </article>
      `,
    )
    .join("");

  const teachers = document.querySelector('[data-render="teachers"]');
  teachers.innerHTML = data.teachers
    .map(
      (item) => `
        <article class="teacher-card">
          <div class="avatar" style="--avatar-a: ${item.colors[0]}; --avatar-b: ${item.colors[1]}">${initials(item.name)}</div>
          <h3>${item.name}</h3>
          <p class="teacher-position">${item.position}</p>
          <div class="teacher-meta">
            <span>${icon("briefcase")} ${item.experience}</span>
            <span>${icon("award")} ${item.achievements}</span>
          </div>
        </article>
      `,
    )
    .join("");

  const career = document.querySelector('[data-render="career"]');
  career.innerHTML = data.career
    .map(
      (item) => `
        <article class="career-card">
          <span class="icon-box">${icon(item.icon)}</span>
          <h3>${item.title}</h3>
          <p>${item.description}</p>
        </article>
      `,
    )
    .join("");
}

function renderProgram() {
  const program = document.querySelector('[data-render="program"]');
  program.innerHTML = data.program
    .map(
      (module, index) => `
        <article class="accordion-item ${index === 0 ? "is-open" : ""}" data-accordion-item>
          <button class="accordion-trigger" type="button" aria-expanded="${index === 0}" data-accordion-trigger>
            <span>
              <span class="accordion-kicker">${module.week}</span>
              <span class="accordion-title">${module.title}</span>
            </span>
            <span class="chevron" aria-hidden="true"></span>
          </button>
          <div class="accordion-panel">
            <ol class="lesson-list">
              ${module.lessons
                .map((lesson, lessonIndex) => `<li><span>${lessonIndex + 1}</span>${lesson}</li>`)
                .join("")}
            </ol>
          </div>
        </article>
      `,
    )
    .join("");
}

function renderPricing() {
  const pricing = document.querySelector('[data-render="pricing"]');
  pricing.innerHTML = data.pricing
    .map(
      (plan) => `
        <article class="price-card ${plan.popular ? "is-popular" : ""}">
          ${plan.popular ? `<div class="popular-label">${icon("star")}Популярный</div>` : ""}
          <h3>${plan.name}</h3>
          <div class="price">
            <strong>${plan.price} ₽</strong>
            <span>за весь курс</span>
          </div>
          <ul class="feature-list">
            ${plan.features.map((feature) => `<li><span>✓</span>${feature}</li>`).join("")}
          </ul>
          <button class="button ${plan.popular ? "button-primary" : "button-secondary"}" type="button">
            Записаться на курс
          </button>
        </article>
      `,
    )
    .join("");
}

function renderFaq() {
  const faq = document.querySelector('[data-render="faq"]');
  faq.innerHTML = data.faq
    .map(
      (item, index) => `
        <article class="accordion-item ${index === 0 ? "is-open" : ""}" data-accordion-item>
          <button class="accordion-trigger" type="button" aria-expanded="${index === 0}" data-accordion-trigger>
            <span class="accordion-title">${item.question}</span>
            <span class="chevron" aria-hidden="true"></span>
          </button>
          <div class="accordion-panel">
            <p>${item.answer}</p>
          </div>
        </article>
      `,
    )
    .join("");
}

function setupAccordions() {
  document.querySelectorAll("[data-accordion-trigger]").forEach((trigger) => {
    trigger.addEventListener("click", () => {
      const item = trigger.closest("[data-accordion-item]");
      const list = item.parentElement;
      const isOpen = item.classList.contains("is-open");

      list.querySelectorAll("[data-accordion-item]").forEach((entry) => {
        entry.classList.remove("is-open");
        entry.querySelector("[data-accordion-trigger]").setAttribute("aria-expanded", "false");
      });

      if (!isOpen) {
        item.classList.add("is-open");
        trigger.setAttribute("aria-expanded", "true");
      }
    });
  });
}

function setupNavigation() {
  const menuButton = document.querySelector("[data-menu-button]");
  const mobileMenu = document.querySelector("[data-mobile-menu]");

  function closeMenu() {
    document.body.classList.remove("menu-open");
    menuButton.classList.remove("is-open");
    mobileMenu.classList.remove("is-open");
    menuButton.setAttribute("aria-expanded", "false");
  }

  menuButton.addEventListener("click", () => {
    const isOpen = mobileMenu.classList.toggle("is-open");
    menuButton.classList.toggle("is-open", isOpen);
    document.body.classList.toggle("menu-open", isOpen);
    menuButton.setAttribute("aria-expanded", String(isOpen));
  });

  document.querySelectorAll("[data-scroll]").forEach((button) => {
    button.addEventListener("click", () => {
      const target = document.getElementById(button.dataset.scroll);
      if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
      closeMenu();
    });
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeMenu();
  });
}

function setupMotionCanvas() {
  const canvas = document.getElementById("motionCanvas");
  if (!canvas) return;

  const context = canvas.getContext("2d");
  const shapes = [
    { x: 0.22, y: 0.3, r: 54, color: "#8b5cf6", speed: 0.9 },
    { x: 0.72, y: 0.34, r: 42, color: "#2dd4bf", speed: 1.2 },
    { x: 0.58, y: 0.7, r: 68, color: "#ec4899", speed: 0.75 },
    { x: 0.34, y: 0.68, r: 34, color: "#f59e0b", speed: 1.45 },
  ];

  function draw(time) {
    const width = canvas.width;
    const height = canvas.height;
    const t = time * 0.001;

    const gradient = context.createLinearGradient(0, 0, width, height);
    gradient.addColorStop(0, "#15152a");
    gradient.addColorStop(0.45, "#10101a");
    gradient.addColorStop(1, "#1f1023");
    context.fillStyle = gradient;
    context.fillRect(0, 0, width, height);

    context.globalAlpha = 0.22;
    context.strokeStyle = "#ffffff";
    context.lineWidth = 1;
    for (let x = 0; x < width; x += 72) {
      context.beginPath();
      context.moveTo(x, 0);
      context.lineTo(x, height);
      context.stroke();
    }
    for (let y = 0; y < height; y += 72) {
      context.beginPath();
      context.moveTo(0, y);
      context.lineTo(width, y);
      context.stroke();
    }

    context.globalAlpha = 1;
    shapes.forEach((shape, index) => {
      const orbitX = Math.cos(t * shape.speed + index) * 42;
      const orbitY = Math.sin(t * shape.speed + index * 0.7) * 34;
      const x = shape.x * width + orbitX;
      const y = shape.y * height + orbitY;

      context.save();
      context.translate(x, y);
      context.rotate(t * shape.speed);
      context.fillStyle = shape.color;
      context.shadowColor = shape.color;
      context.shadowBlur = 28;

      if (index % 2 === 0) {
        context.fillRect(-shape.r, -shape.r * 0.62, shape.r * 2, shape.r * 1.24);
      } else {
        context.beginPath();
        context.arc(0, 0, shape.r, 0, Math.PI * 2);
        context.fill();
      }

      context.restore();
    });

    context.globalAlpha = 0.92;
    context.fillStyle = "#ffffff";
    context.font = "700 34px Inter, system-ui, sans-serif";
    context.fillText("MOTION", width * 0.1, height * 0.84);
    context.globalAlpha = 0.62;
    context.font = "500 18px Inter, system-ui, sans-serif";
    context.fillText("2D / 3D / showreel", width * 0.1, height * 0.9);
    context.globalAlpha = 1;

    requestAnimationFrame(draw);
  }

  requestAnimationFrame(draw);
}

renderCards();
renderProgram();
renderPricing();
renderFaq();
setupAccordions();
setupNavigation();
setupMotionCanvas();
