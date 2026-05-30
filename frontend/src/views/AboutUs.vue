<template>
  <main class="about-page">
    <div class="about-hero">
      <div>
        <h1 class="about-hero__title-ru">О НАС</h1>
        <h1 class="about-hero__title-eng">Bon's Burgers</h1>
        <p class="about-hero__subtitle">История о мечте, инновациях и наследии, которое переживёт поколения</p>
      </div>
    </div>

    <section class="about-intro">
      <div class="about-intro__text">
        <p>
          Наша история началась в <strong>1958 году</strong>, когда два студента колледжа — 
          <strong>Джек Уолтен</strong> и <strong>Феликс Кранкен</strong> — познакомились и подружились. 
          Их общая страсть к технологиям и развлечениям привела к созданию одной из самых 
          амбициозных концепций ресторанного бизнеса того времени.
        </p>
        <p>
          При поддержке <strong>Cyberfun Tech</strong> — пионера технологических инноваций, основанного ещё в 1943 году Джейсоном Пултриком — Джек и Феликс получили возможность 
          воплотить свою мечту в жизнь. <strong>28 июня 1974 года</strong> ресторан Bon's Burgers 
          впервые открыл свои двери для посетителей в Брайтоне, штат Мичиган.
        </p>
      </div>
    </section>

    <section class="timeline-section">
      <h2 class="timeline-section__title">ПОДРОБНАЯ ХРОНОЛОГИЯ</h2>
      
      <div class="timeline-era">
        <div class="timeline-item">
          <div class="timeline-item__year">1889</div>
          <div class="timeline-item__content">
            <p>Рождение <strong>Джейсона Пултрика</strong> — будущего основателя Cyberfun Tech, компании, которая позже станет ключевым партнёром Bon's Burgers.</p>
          </div>
        </div>

        <div class="timeline-item">
          <div class="timeline-item__year">1932</div>
          <div class="timeline-item__content">
            <p><strong>23 сентября:</strong> родился <strong>Джек Уолтен</strong> — будущий сооснователь и визионер проекта Bon's Burgers.</p>
          </div>
        </div>

        <div class="timeline-item">
          <div class="timeline-item__year">1934</div>
          <div class="timeline-item__content">
            <p><strong>20 апреля:</strong> родилась <strong>Розмари Уолтен</strong> (девичья фамилия неизвестна) — жена Джека.</p>
          </div>
        </div>

        <div class="timeline-item">
          <div class="timeline-item__year">1935</div>
          <div class="timeline-item__content">
            <p>Рождение <strong>Феликса Кранкена</strong> — второго сооснователя Bon's Burgers и технического гения проекта.</p>
          </div>
        </div>

        <div class="timeline-item">
          <div class="timeline-item__year">1943</div>
          <div class="timeline-item__content">
            <p>Джейсон Пултрик основывает <strong>Cyberfun Tech</strong> — компанию, которая станет пионером в области развлекательных технологий.</p>
          </div>
        </div>
        
        <div class="timeline-item">
          <div class="timeline-item__year">1958</div>
          <div class="timeline-item__content">
            <p>Джек Уолтен и Феликс Кранкен, встретившись в колледже, задумывают концепцию <strong>Bon's Burgers</strong>. Рождение идеи — создать ресторан, где еда встречается с магией аниматронных развлечений.</p>
          </div>
        </div>

        <div class="timeline-item">
          <div class="timeline-item__year">1960</div>
          <div class="timeline-item__content">
              <p>Cyberfun Tech запускает выставку <em>«Технологии будущего»</em> (Technology of the Future).</p>
          </div>
        </div>

        <div class="timeline-item">
          <div class="timeline-item__year">1965</div>
          <div class="timeline-item__content">
              <p>Джек и Феликс представляют проект руководству Cyberfun Tech. Сделка заключена в период 1965-1967 гг.</p>
          </div>
        </div>
        
        <div class="timeline-item">
          <div class="timeline-item__year">1967</div>
          <div class="timeline-item__content">
            <p><strong>15 апреля:</strong> Феликс Кранкен записывает корпоративное приветствие для <strong>Bunny Smiles Inc.</strong> — официального оператора Bon's Burgers.</p>
          </div>
        </div>

        <div class="timeline-item">
          <div class="timeline-item__year">1970</div>
          <div class="timeline-item__content">
            <p><strong>25 декабря:</strong> Розмари и Джек дарят Эдду и Молли на Рождество серую куклу кролика <strong>"Rocket"</strong>.</p>
          </div>
        </div>

        <div class="timeline-item">
          <div class="timeline-item__year">1972</div>
          <div class="timeline-item__content">
            <p><strong>10 декабря:</strong> Феликс записывает очередное сообщение для компании.</p>
          </div>
        </div>
      </div>
    </section>

    <div class="about-buttons">
      <router-link to="/stars">
        <button class="about-btn">★Встретить аниматроников★</button>
      </router-link>
      <router-link to="/menu">
        <button class="about-btn">★Посмотреть меню★</button>
      </router-link>
    </div>
  </main>
</template>

<script setup>
</script>

<style scoped src="@/assets/styles/views/AboutUs.css">

</style>