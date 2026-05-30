<template>
    <header class="header">
        <div class="header__logo">
            <router-link to="/" class="header__llink">
                <template v-if="logoLoading">
                    <div class="header__logo-skeleton"></div>
                </template>
                <template v-else-if="logoError">
                    <div class="header__logo-error">🍔</div>
                </template>
                
                <template v-else>
                    <img 
                        :src="logoUrl" 
                        alt="Bon's Burgers лого" 
                        class="header__llink-img"
                        @error="handleLogoError"
                        crossorigin="anonymous"
                    />
                </template>
                
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
            <router-link 
                v-if="loggedIn" 
                to="/profile/cart" 
                class="nav-link" 
                active-class="active"
            >
                Корзина
            </router-link>
        </nav>
        <div class="header__search-container" ref="searchContainer">
            <input 
                type="text" 
                v-model="searchQuery"
                @input="handleInput"
                @focus="showResults = true"
                @keydown.enter="navigateToFirst"
                @keydown.escape="closeSearch"
                placeholder="Поиск по сайту..."
                class="header__search-input"
            >
            <div v-if="showResults && searchResults.length > 0" class="search-dropdown">
                <div 
                    v-for="item in searchResults" 
                    :key="item.id" 
                    class="search-item"
                    @click="goTo(item)"
                >
                    <img :src="item.image" alt="" class="search-item-img" v-if="item.image">
                    <div class="search-item-text">
                        <span class="search-item-title">{{ item.title }}</span>
                        <span class="search-item-cat">{{ item.type_label }}</span>
                    </div>
                </div>
            </div>
        </div>
        <div>
            <div class="header__profile" v-if="loggedIn">
                <div class="header__avatar" @click="toggleDropdown" ref="avatarRef">
                    <span class="header__avatar-letter">{{ userInitial }}</span>
            
                    <div class="header__dropdown" v-if="isDropdown" @click="ProfileOpener">
                        <div class="dropdown__header">
                            <span class="dropdown__avatar-letter">{{ userInitial }}</span>
                            <div class="dropdown__user-info">
                                <span class="dropdown__username">{{ user?.username }}</span>
                            </div>
                        </div>
            
                        <div class="dropdown__divider"></div>
            
                        <router-link to="/profile" class="dropdown__link" @click="closeDropdown">Профиль</router-link>
                        <router-link v-if="isAdmin" to="/admin" class="dropdown__link dropdown__admin" @click="closeDropdown">
                            Админ-панель
                        </router-link>

                        <button @click="logout" class="dropdown__link dropdown__logout">Выйти</button>
                    </div>
                </div>
            </div>
            <router-link to="/auth/login" class="header__login" v-else>
                <template v-if="loginIconLoading">
                    <div class="header__login-icon-skeleton"></div>
                </template>
                <template v-else-if="loginIconError">
                    <div class="header__login-icon-error">🔐</div>
                </template>
                <template v-else>
                    <img 
                        :src="loginIconUrl" 
                        alt="Значок входа в аккаунт" 
                        class="header__login-img"
                        @error="handleLoginIconError"
                        crossorigin="anonymous"
                    >
                </template>
                
                <span class="header__login-text">Авторизация</span>
            </router-link>
        </div>
    </header>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Header',
    data() {
        return {
            isDropdown: false,
            user: null,
            searchQuery: '',
            searchResults: [],
            showResults: false,
            searchTimer: null,
            logoUrl: null,
            logoLoading: true,
            logoError: false,
            loginIconUrl: null,
            loginIconLoading: true,
            loginIconError: false
        }
    },
    computed: {
        loggedIn() {
            return !!localStorage.getItem('authToken') && !!localStorage.getItem('user')
        },
        userInitial() {
            const userStr = localStorage.getItem('user')
            if (!userStr) return ''
            try {
                const user = JSON.parse(userStr)
                return user.username?.charAt(0).toUpperCase() || ''
            } catch {
                return ''
            }
        },
        isAdmin() {
            try {
                const user = JSON.parse(localStorage.getItem('user') || '{}')
                return user.role === 'admin'
            } catch {
                return false
            }
        }
    },
    created() {
        this.loadUser()
        this.fetchLogo()
        this.fetchLoginIcon()
        this.fetchCartCount()
    },
    mounted() {
        document.addEventListener('click', this.handleClickOutside)
    },
    beforeUnmount() {
        document.removeEventListener('click', this.handleClickOutside)
    },
    methods: {
        async fetchLogo() {
            this.logoLoading = true
            this.logoError = false
            try {
                const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'
                const res = await axios.get(`${API_BASE}/home/logo`)
                this.logoUrl = res.data.imageUrl || res.data.logo || res.data
            } catch (e) {
                console.warn('Не удалось загрузить логотип:', e)
                this.logoError = true
            } finally {
                this.logoLoading = false
            }
        },
        async fetchLoginIcon() {
            this.loginIconLoading = true
            this.loginIconError = false
            try {
                const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'
                const res = await axios.get(`${API_BASE}/home/login-icon`)
                this.loginIconUrl = res.data.imageUrl || res.data.icon || res.data
            } catch (e) {
                console.warn('Не удалось загрузить иконку входа:', e)
                this.loginIconError = true
            } finally {
                this.loginIconLoading = false
            }
        },
        async fetchCartCount() {
            if (!this.loggedIn) {
                return
            }
            try {
                const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'
                const token = localStorage.getItem('authToken')
                const res = await axios.get(`${API_BASE}/cart`, {
                    headers: { Authorization: `Bearer ${token}` }
                })
                const items = res.data.items || res.data || []
                this.cartCount = items.reduce((sum, item) => sum + (item.quantity || 1), 0)
            } catch (e) {
                console.warn('Не удалось загрузить корзину:', e)
            }
        },
        handleLogoError() {
            this.logoError = true
            this.logoLoading = false
        },
        handleLoginIconError() {
            this.loginIconError = true
            this.loginIconLoading = false
        },
        
        loadUser() {
            const userData = localStorage.getItem('user')
            if (userData) this.user = JSON.parse(userData)
        },
        toggleDropdown() {
            this.isDropdown = !this.isDropdown
        },
        closeDropdown() {
            this.isDropdown = false
        },
        ProfileOpener() {},
        logout() {
            this.isDropdown = false
            localStorage.removeItem('authToken')
            localStorage.removeItem('user')
            window.location.href = '/'
        },
        handleInput() {
            clearTimeout(this.searchTimer)
            this.showResults = true
            this.searchTimer = setTimeout(() => {
                if (this.searchQuery.length >= 2) {
                    this.fetchSearch()
                } else {
                    this.searchResults = []
                }
            }, 300)
        },
        async fetchSearch() {
            try {
                const encodedQuery = encodeURIComponent(this.searchQuery)
                const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'
                const res = await axios.get(`${API_BASE}/search?q=${encodedQuery}`)
                this.searchResults = res.data
            } catch (e) {
                console.error('Ошибка поиска:', e)
                this.searchResults = []
            }
        },
        goTo(item) {
            this.$router.push(item.route)
            this.closeSearch()
        },
        navigateToFirst() {
            if (this.searchResults.length > 0) {
                this.goTo(this.searchResults[0])
            }
        },
        closeSearch() {
            this.showResults = false
        },
        handleClickOutside(event) {
            if (this.$refs.avatarRef && !this.$refs.avatarRef.contains(event.target)) {
                this.closeDropdown()
            }
            if (this.$refs.searchContainer && !this.$refs.searchContainer.contains(event.target)) {
                this.closeSearch()
            }
        }
    }
}
</script>

<style scoped src="@/assets/styles/components/Header.css">

</style>