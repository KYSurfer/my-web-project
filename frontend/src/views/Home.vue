<template>
    <main class="main-content">
        <div class="main-content__welcome">
            <div>
                <h1 class="main-content__welcome-ru">Добро пожаловать в</h1>
                <h1 class="main-content__welcome-eng">Bon's Burgers</h1>
                <p class="main-content__welcome-par">В наших ресторанах не только много вкусной еды, но и множество развлечений, которые вам не найти нигде на свете. Bon's Burgers — место, где еда — это только начало приключений.</p>
            </div>
            <div class="main-content__welcome-img-wrapper">
                <img src="..\assets\images\welcome-image.png" alt="Бон" class="main-content__welcome-img">
            </div>
        </div>

        <div class="main-content__second">
            <h1 class="main-content__important-txt">Наша удивительная команда аниматроников</h1>
            <p class="main-content__animatronic-desc">Встречайте тех, кто делает Bons Burgers по-настоящему живым и весёлым местом!</p>
            <div class="main-content__block-second">
                <div class="main-content__b">
                    <div class="main-content__block">
                        <img src="../assets/images/bon-frontpage.jpg" alt="bon" class="main-content__block-img">
                        <h1 class="main-content__block-name">Bon the Rabbit</h1>
                        <h3 class="main-content__block-alias">►►Главный Маскот</h3>
                        <p>Синий кролик-аниматроник и главный талисман Bon's Burgers. Лицо ресторана.</p>
                        <button>►Узнать больше!</button>
                    </div>
                    <div class="main-content__block">
                        <img src="..\assets\images\banny-frontpage.png" alt="banny" class="main-content__block-img">
                        <h1 class="main-content__block-name">Banny the Hare</h1>
                        <h3 class="main-content__block-alias">►►Веселая зайчиха</h3>
                        <p>Фиолетовый кролик-аниматроник, сестра Бона. Известна своим музыкальным талантом.</p>
                        <button>►Узнать больше!</button>
                    </div>
                    <div class="main-content__block">
                        <img src="..\assets\images\Sha-frontpage.jpg" alt="sha" class="main-content__block-img">
                        <h1 class="main-content__block-name">Sha the Sheep</h1>
                        <h3 class="main-content__block-alias">►►Милая овечка</h3>
                        <p>Овца-аниматроник с пушистой шерстью. Добрая душа группы.</p>
                        <button>►Узнать больше!</button>
                    </div>
                    <div class="main-content__block">
                        <img src="..\assets\images\boozoo-frontpage.jpg" alt="boozoo" class="main-content__block-img">
                        <h1 class="main-content__block-name">Boozoo the Showmaster</h1>
                        <h3 class="main-content__block-alias">►►Лучший ведущий</h3>
                        <p>Аниматроник с магическими способностями и в красной куртке.</p>
                        <button>►Узнать больше!</button>
                    </div>
                </div>
            </div>
            <router-link to="/stars">
                <button class="main-content__meet-all">★Встретить их всех★</button>
            </router-link>
        </div>

        <div class="main-content__third">
            <h1 class="main-content__important-txt">Выбор покупателей</h1>
            <p class="main-content__animatronic-desc">Топ-3 товара по версии наших гостей!</p>
            
            <div v-if="loading" class="main-content__loading">
                <p>Загрузка лучших товаров...</p>
            </div>

            <div v-else-if="bestProducts.length > 0" class="main-content__b">
                <div 
                    v-for="(product, index) in bestProducts" 
                    :key="product.id" 
                    class="main-content__block best-product-card"
                >
                    
                    <img :src="product.image" :alt="product.name" class="main-content__block-img">
                    <h1 class="main-content__block-name">{{ product.name }}</h1>
                    <h3 class="main-content__block-alias">{{ product.category }}</h3>
                    <p>{{ product.description }}</p>
                    
                    <div class="likes-counter">
                        <span class="heart-icon"></span>
                        <span>{{ product.likes }}</span>
                    </div>
                    
                    <button @click="goToProduct(product.id)">Подробнее</button>
                </div>
            </div>

            <div v-else class="main-content__no-products">
                <p>Пока нет товаров с лайками</p>
            </div>
        </div>

        <router-link to="/menu">
            <button class="main-content__meet-all">★Посмотреть всё меню★</button>
        </router-link>
    </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const bestProducts = ref([])
const loading = ref(true)

const fetchBestProducts = async () => {
    try {
        const response = await axios.get('http://localhost:5000/api/products/best')
        if (response.data.success) {
            bestProducts.value = response.data.data
        }
    } catch (error) {
        console.error('Ошибка загрузки:', error)
    } finally {
        loading.value = false
    }
}

const goToProduct = (id) => {
    router.push(`/product/${id}`)
}

onMounted(() => {
    fetchBestProducts()
})
</script>

<style>
.main-content {
    padding-top: 300px;
    background-color: black;
}

.main-content__welcome{
    display: flex;
    padding-left: 300px;
}

.main-content__welcome-ru{
    font-family: 'Uncage', sans-serif;
    font-size: 50px;
    color:aliceblue;
    max-width: 500px;
    text-shadow: -5px 5px 0 var(--blood-red);
}

.main-content__welcome-eng{
    font-family: 'Dessau-Heavy', sans-serif;
    font-size: 70px;
    color: var(--vintage-yellow);
    margin-top: -30px;
    max-width: 500px;
    text-shadow: -5px 5px 0 var(--blood-red);
}

.main-content__welcome-img {
    width: 100%;
    display: block;
    border: 3px solid var(--vintage-yellow);
}

.main-content__welcome-par{
    margin-top: 20px;
    max-width: 700px;
    font-size: 20px;
    gap: 20px;
    line-height: 1.5;
    font-family: 'Uncage', sans-serif;
    color: rgb(223, 223, 223);
}

.main-content__second{
    justify-content: center;
}

.main-content__second{
    gap: 50px;
    text-align: center;
    margin-top: 200px;
}

.main-content__b {
    display: flex;
    gap: 50px;
    justify-content: center;
}

.main-content__important-txt{
    font-family: 'Uncage', sans-serif;
    color: rgb(223, 223, 223);
    font-size: 40px;
    text-shadow: -5px 5px 0 var(--bon-blue-dark);
}

.main-content__animatronic-desc{
    margin-top: 20px;
    margin-bottom: 80px;
    font-family: 'Uncage', sans-serif;
    color: rgb(223, 223, 223);
    font-size: 20px;
}

.main-content__block{
    width: 100px;
    font-family: 'Uncage', sans-serif;
    color: rgb(223, 223, 223);
    font-size: 20px;
    margin: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    border: 3px solid var(--vintage-yellow);
    box-shadow: 5px 5px var(--blood-red);
    padding-inline: 150px;
    gap: 15px;
}

.main-content__block-img{
    border: 3px solid var(--vintage-yellow);
    width: 300px;
}

.main-content__block-alias{
    font-family: 'EkiR', sans-serif;
    font-size: 13px;
    color: rgb(167, 161, 161);
}

.main-content__welcome-img-wrapper {
    box-shadow: 0 0 100px rgba(218, 10, 10, 1);
    width: 500px;
    margin-left: 150px;
    padding: 5px;
}

.main-content__meet-all{
    margin-top: 30px;
    padding: 20px;
    background-color: var(--vintage-yellow);
    box-shadow: 5px 5px 0 var(--blood-red);
    font-family: 'Uncage', sans-serif;
    color: black;
    font-size: 20px;
}

.main-content__block-second{
    margin-bottom: 150px;
}

.best-product-badge {
    position: absolute;
    top: -15px;
    left: 50%;
    transform: translateX(-50%);
    background: linear-gradient(135deg, var(--vintage-yellow) 0%, var(--blood-red) 100%);
    color: black;
    padding: 8px 20px;
    border-radius: 20px;
    font-family: 'Uncage', sans-serif;
    font-weight: bold;
    font-size: 14px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    z-index: 10;
}

.best-product-card {
    position: relative;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.best-product-card:hover {
    transform: translateY(-10px);
    box-shadow: 10px 10px var(--blood-red);
}

.likes-counter {
    display: flex;
    align-items: center;
    gap: 8px;
    background: rgba(218, 10, 10, 0.3);
    padding: 8px 16px;
    border-radius: 20px;
    font-family: 'Uncage', sans-serif;
    font-size: 16px;
    color: var(--vintage-yellow);
}

.heart-icon {
    font-size: 18px;
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.2); }
}

.main-content__block button {
    margin-top: 10px;
    padding: 12px 30px;
    background-color: var(--vintage-yellow);
    border: none;
    box-shadow: 3px 3px 0 var(--blood-red);
    font-family: 'Uncage', sans-serif;
    color: black;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.main-content__block button:hover {
    transform: translate(-2px, -2px);
    box-shadow: 5px 5px 0 var(--blood-red);
}

.main-content__loading,
.main-content__no-products {
    text-align: center;
    padding: 50px;
    font-family: 'Uncage', sans-serif;
    color: rgb(223, 223, 223);
    font-size: 20px;
}

@media (max-width: 1200px) {
    .main-content__b {
        flex-wrap: wrap;
    }
    
    .main-content__block {
        padding-inline: 50px;
    }
}

@media (max-width: 768px) {
    .main-content__block {
        width: 90%;
        padding-inline: 20px;
    }
    
    .main-content__block-img {
        width: 200px;
    }
}
</style>