<template>
    <main class="register">
        <router-link to="/" class="register__link">
            <div class="register__back">
                <span class="register__back-txt">◄ На главную</span>  
            </div>
        </router-link>

        <div class="register__form">
            <div class="register__form-info">
                <div class="register__form-info-head">
                    <h1 class="register__form-info-header">Создание аккаунта</h1>
                    <h3 class="register__form-info-undertext">Добро пожаловать!</h3>
                </div>
                <form @submit.prevent="handleSubmit">
                    <div class="register__form-info-username">
                        <label class="register__form-info-username-txt">Имя пользователя</label>
                        <input 
                            type="text" 
                            v-model="form.username" 
                            placeholder="►► Имя" 
                            class="register-input" 
                            required
                        >
                    </div>

                    <div class="register__form-info-email">
                        <label class="register__form-info-email-txt">Email</label>
                        <input 
                            type="email" 
                            v-model="form.email" 
                            placeholder="►► Email" 
                            class="register-input" 
                            required
                        >
                    </div>

                    <div class="register__form-info-password">
                        <label class="register__form-info-password-txt">Пароль</label>
                        <input 
                            type="password" 
                            v-model="form.password" 
                            placeholder="►► Пароль" 
                            class="register-input" 
                            required
                            minlength="6"
                        >
                    </div>

                    <button 
                        type="submit" 
                        :disabled="isLoading" 
                        class="register__btn"
                    >
                        {{ isLoading ? 'Регистрация...' : '► Зарегистрироваться' }}
                    </button>
                </form>
                
                <div class="register__login-link">
                    <span>Уже есть аккаунт?</span>
                    <router-link to="/auth/login">Войти</router-link>
                </div>

                <div class="register__toast error" v-if="serverError">
                    {{ serverError }}
                </div>
            </div>

            <div>
                <img src="../assets/images/Bons.webp" alt="Bons Burger restaurant photo" class="register__img">
            </div>
        </div>
    </main>
</template>

<script>
import api from '@/plugins/axios'

export default {
    name: 'Register',
    data() {
        return {
            form: { username: '', email: '', password: '' },
            isLoading: false,
            serverError: '' 
        }
    },
    methods: {
        async handleSubmit() {
            this.serverError = ''
            this.isLoading = true

            try {
                const response = await api.post('/auth/register', this.form)
                
                localStorage.setItem('authToken', response.data.token)
                localStorage.setItem('user', JSON.stringify(response.data.user))
                
                this.$router.push('/profile')
            } catch (error) {
                this.serverError = error.response?.data?.message || 'Ошибка регистрации'
            } finally {
                this.isLoading = false
            }
        }
    }
}
</script>

<style>
.register {
    background: linear-gradient(135deg, #0a0a0a 0%, #2d4a55 50%, #4a2d55 100%);
    min-height: 100vh;
    width: 100%;
    overflow-x: hidden;
}

.register-input::-moz-placeholder {
    font-family: 'EkiR', sans-serif !important;
    font-size: 7px !important;
    color: #999 !important;
    opacity: 1 !important;
}

.register__link {
    text-decoration: none;
}

.register__back {
    padding-top: 20px;
    padding-left: 20px;
    text-decoration: none;
}

.register__back-txt {
    font-family: 'Uncage';
    text-decoration: none;
    color: gray;
}

.register__form {
    margin: 200px auto;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 50px;
    padding: 50px;
    border-radius: 30px;
    box-shadow: 0 0 40px rgba(196, 177, 2, 0.644);
    width: fit-content;
    max-width: 100%;
}

.register__form-info {
    display: flex;
    flex-direction: column;
    gap: 30px;
}

.register__form-info-head {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.register__form-info-header {
    color: aliceblue;
    font-family: 'Uncage';
}

.register__form-info-undertext {
    font-family: 'EkiR';
    color: gray;
    font-size: 10px;
}

.register__form-info-email,
.register__form-info-password,
.register__form-info-username {
    font-family: 'Uncage';
}

.register-input {
    font-family: 'Uncage', sans-serif;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.register__form-info-password-txt,
.register__form-info-email-txt,
.register__form-info-username-txt {
    color: white;
}

.register__img {
    height: 500px;
    border-top-right-radius: 30px;
    border-bottom-right-radius: 30px;
}

.register__btn {
    padding: 15px;
    background: var(--vintage-yellow, #f4d03f);
    color: black;
    border: none;
    font-size: 18px;
    cursor: pointer;
    border-radius: 5px;
    font-family: 'Uncage', sans-serif;
}

.register__btn:hover {
    transform: translate(-2px, -2px);
    box-shadow: 4px 4px 0 var(--blood-red, #8b0000);
}

.register__btn:disabled {
    background: gray;
    cursor: not-allowed;
}

.register__login-link {
    text-align: center;
    color: gray;
    font-family: 'Uncage';
}

.register__login-link a {
    color: var(--vintage-yellow, #f4d03f);
    text-decoration: none;
}

.register__toast.error {
    padding: 15px;
    background: var(--blood-red, #8b0000);
    color: white;
    border-radius: 5px;
    text-align: center;
    font-family: 'Uncage';
}
</style>