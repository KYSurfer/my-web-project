<template>
    <main class="login">
        <router-link to="/" class="login__link">
            <div class="login__back">
                <span class="login__back-txt">◄ На главную</span>  
            </div>
        </router-link>
        <div class="login__form">
            <div class="login__form-info">
                <div class="login__form-info-head">
                    <h1 class="login__form-info-header">Вход в аккаунт</h1>
                    <h3 class="login__form-info-undertext">Мы тебя ждали!</h3>
                </div>
                
                <form @submit.prevent="handleSubmit">
                    <div class="login__form-info-email">
                        <label class="login__form-info-email-txt">Email</label>
                        <input type="email" placeholder="►► Email" v-model="form.email" class="login-input" required>
                    </div>
                    <div class="login__form-info-password">
                        <label class="login__form-info-password-txt">Пароль</label>
                        <input type="password" placeholder="►► Пароль" v-model="form.password" class="login-input" required>
                    </div>
                    <button type="submit" :disabled="isLoading" class="login__btn">{{ isLoading ? 'Вход...' : '► Войти' }}</button>
                </form>
                <div>
                    <span>У меня нет аккаунта?</span>
                    <router-link to="/auth/register">Создать аккаунт</router-link>
                </div>
            </div>
            <div>
                <img src="../assets/images/Bons.webp" alt="Bons Burger restaraunt photo" class="login__img">
            </div>
        </div>
    </main>
</template>

<script>
import api from '@/plugins/axios'

export default {
    name: 'Login',
    data() {
        return{
            form: { email: '', password: ''},
            isLoading: false,
            serverError: ''
        }
    },
    methods: {
        async handleSubmit() {
            this.serverError = ''
            this.isLoading = true

            try {
                const response = await api.post('/auth/login', this.form)

                localStorage.setItem('authToken', response.data.token)
                localStorage.setItem('user', JSON.stringify(response.data.user))

                this.$router.push('/profile')
            }
            catch (error){
                this.serverError = error.response?.data?.message || 'Ошибка входа'
            } finally {
                this.isLoading = false
            }
        }
    }
}

</script>

<style>
.login-input::-moz-placeholder {
    font-family: 'EkiR', sans-serif !important;
    font-size: 7px !important;
    color: #999 !important;
    opacity: 1 !important;
}

.login__link {
    text-decoration: none;
}

.login__back {
    padding-top: 20px;
    padding-left: 20px;
    text-decoration: none;
}

.login__back-txt {
    font-family: 'Uncage';
    text-decoration: none;
    color: gray;
}

.login {
    background: linear-gradient(135deg, #0a0a0a 0%, #2d4a55 50%, #4a2d55 100%);
    min-height: 100vh;
    width: 100%;
    overflow-x: hidden;
}

.login__form {
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

.login__form-info {
    display: flex;
    flex-direction: column;
    gap: 30px;
}

.login__form-info-head {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.login__form-info-header {
    color: aliceblue;
    font-family: 'Uncage';
}

.login__form-info-undertext {
    font-family: 'EkiR';
    color: gray;
    font-size: 10px;
}

.login__form-info-email,
.login__form-info-password {
    font-family: 'Uncage';
}

.login-input {
    font-family: 'Uncage', sans-serif;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.login__form-info-password-txt,
.login__form-info-email-txt{
    color: white;
}

.login__img{
    height: 500px;
    border-top-right-radius: 30px;
    border-bottom-right-radius: 30px;
}

.login__btn {
    padding: 15px;
    background: var(--vintage-yellow, #f4d03f);
    color: black;
    border: none;
    font-size: 18px;
    cursor: pointer;
    border-radius: 5px;
    font-family: 'Uncage', sans-serif;
}

.login__btn:hover {
    transform: translate(-2px, -2px);
    box-shadow: 4px 4px 0 var(--blood-red, #8b0000);
}

.login__btn:disabled {
    background: gray;
    cursor: not-allowed;
}

.login__register-link {
    text-align: center;
    color: gray;
    font-family: 'Uncage';
}

.login__register-link a {
    color: var(--vintage-yellow, #f4d03f);
    text-decoration: none;
}
</style>