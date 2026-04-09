<template>
    <header class="header">
        <div class="header__logo">
            <router-link to="/" class="header__llink">
                <img src="../assets/images/bons-burgers-logo-removebg.png" alt="Bon's Burgers лого" class="header__llink-img"/>
                <span class="header__llink-text">BON'S BURGERS</span>
            </router-link>
        </div>
        <nav class="header__nav">
            <router-link to="/" class="nav-link" active-class="active">Главная</router-link>
            <router-link to="/stars" class="nav-link" active-class="active">Наши звезды</router-link>
            <router-link to="/menu" class="nav-link" active-class="active">Меню</router-link>
            <router-link to="/merch" class="nav-link" active-class="active">Товары</router-link>
            <router-link to="/cast" class="nav-link" active-class="active">Персонал</router-link>
            <router-link to="/about-us" class="nav-link" active-class="active">О нас</router-link>
        </nav>
        <div class="header__search-container">
            <input type="text">
        </div>
        <div>
            <!-- ✅ ЗАМЕНИТЕ пустой div на это -->
            <div class="header__profile" v-if="loggedIn">
                <div 
                    class="header__avatar" 
                    @click="toggleDropdown"
                    ref="avatarRef"
                >
            <span class="header__avatar-letter">
                {{ userInitial }}
            </span>
        
            <div class="header__dropdown" v-if="isDropdown" v-on:click="ProfileOpener">
                        <div class="dropdown__header">
                        <span class="dropdown__avatar-letter">{{ userInitial }}</span>
                            <div class="dropdown__user-info">
                                <span class="dropdown__username">{{ user?.username }}</span>
                                <span class="dropdown__email">{{ user?.email }}</span>
                            </div>
                        </div>
            
                        <div class="dropdown__divider"></div>
            
                        <router-link to="/profile" class="dropdown__link" @click="closeDropdown">
                            👤 Профиль
                        </router-link>
            
                        <button @click="logout" class="dropdown__link dropdown__logout">
                            🚪 Выйти
                        </button>
                    </div>
                </div>
            </div>
            <router-link to="/auth/login" class="header__login" v-else>
                <img src="@/assets/images/user-icon.png" alt="Значок входа в аккаунт" class="header__login-img">
                <span class="header__login-text">Авторизация</span>
            </router-link>
        </div>
        </header>
</template>

<script>
export default {
    name: 'Header',
    data() {
        return {
            isDropdown: false,
            user: null
        }
    },
    computed: {
        loggedIn() {
            return !!localStorage.getItem('authToken')
        },
        userInitial() {
            return this.user?.username?.charAt(0).toUpperCase() || 'U'
        }
    },
    
    mounted() {
        this.loadUser()
        document.addEventListener('click', this.handleClickOutside)
    },
    
    beforeUnmount() {
        document.removeEventListener('click', this.handleClickOutside)
    },
    
    methods: {
        loadUser() {
            const userData = localStorage.getItem('user')
            if (userData) {
                this.user = JSON.parse(userData)
            }
        },
        toggleDropdown() {
            this.isDropdown = !this.isDropdown
        },
        closeDropdown() {
            this.isDropdown = false
        },
        handleClickOutside(event) {
            if (this.$refs.avatarRef && !this.$refs.avatarRef.contains(event.target)) {
                this.closeDropdown()
            }
        },
        logout() {
            localStorage.removeItem('authToken')
            localStorage.removeItem('user')
            this.user = null
            this.closeDropdown()
            this.$router.push('/')
        },
        
    }
}
</script>

<style scoped>
.header {
    width: 100%;
    position: fixed;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: black;
    box-shadow: 0 0px 30px var(--vintage-yellow);
}

.header__logo {
    margin-block: 10px;
    margin-right: 10px;
    font-size: 20px;
}

.header__llink {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-decoration: none;
} 

.header__llink-img {
    height: 60px;
}

.header__llink-text {
    font-family: 'Dessau-Heavy', sans-serif;
    color: rgb(223, 226, 6);
    text-shadow: -2px 1px 0 rgb(230, 3, 3);
}

.header__nav{
    margin-left: 40px;
    display: flex;
    gap: 50px;
    font-family: 'Uncage', sans-serif;
    color: gray;
    font-size: 18px;
}

.header__search-container{
    margin-left: 100px;
}

.header__login{
    gap: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-left: 60px;
    text-decoration: none;
}

.header__login-img{
    height: 60px;
}

.header__login-text{
    font-family: 'Uncage', sans-serif;
    color: gray;
    text-decoration: none;
}

/* 🔥 Добавьте эти стили в конец вашего <style> */

.header__profile {
    position: relative;
    margin-left: 60px;
}

.header__avatar {
    width: 45px;
    height: 45px;
    border-radius: 50%;
    background: var(--vintage-yellow, #f4d03f);
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    border: 2px solid var(--blood-red, #8b0000);
    position: relative;
}

.header__avatar-letter {
    font-family: 'Uncage', sans-serif;
    font-size: 20px;
    color: black;
    font-weight: bold;
}

.header__dropdown {
    position: absolute;
    top: 60px;
    right: 0;
    width: 280px;
    background: rgba(10, 10, 10, 0.98);
    border: 2px solid var(--vintage-yellow, #f4d03f);
    border-radius: 10px;
    padding: 15px;
    z-index: 1001;
}

.dropdown__header {
    display: flex;
    gap: 15px;
    align-items: center;
    padding-bottom: 15px;
}

.dropdown__avatar-letter {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: var(--vintage-yellow, #f4d03f);
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: 'Uncage', sans-serif;
    font-size: 24px;
    color: black;
}

.dropdown__user-info {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.dropdown__username {
    font-family: 'Uncage', sans-serif;
    color: white;
    font-size: 16px;
}

.dropdown__email {
    font-family: 'EkiR', sans-serif;
    color: gray;
    font-size: 12px;
}

.dropdown__divider {
    height: 1px;
    background: var(--blood-red, #8b0000);
    margin: 10px 0;
}

.dropdown__link {
    display: block;
    padding: 12px 15px;
    font-family: 'Uncage', sans-serif;
    color: rgb(223, 223, 223);
    text-decoration: none;
    background: transparent;
    border: none;
    cursor: pointer;
    width: 100%;
    text-align: left;
}

.dropdown__link:hover {
    background: var(--blood-red, #8b0000);
    color: white;
}

.dropdown__logout {
    color: var(--blood-red, #8b0000);
}
</style>