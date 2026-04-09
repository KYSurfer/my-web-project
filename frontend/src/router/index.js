import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue'
import AboutUs from '../views/AboutUs.vue'
import Stars from '../views/Stars.vue'
import Merch from '../views/Merch.vue'
import News from '../views/News.vue'
import Cast from '../views/Cast.vue'
import Menu from '../views/Menu.vue'
import Login from "../views/Login.vue"
import Register from '../views/Register.vue'
import Profile from '../views/Profile.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about-us',
    name: 'About-us',
    component: AboutUs
  },
  {
    path: '/stars',
    name: 'Stars',
    component: Stars
  },
  {
    path: '/merch',
    name: 'Merch',
    component: Merch
  },
  {
    path: '/news',
    name: 'News',
    component: News
  },
  {
    path: '/cast',
    name: 'Cast',
    component: Cast
  },
  {
    path: '/menu',
    name: 'Menu',
    component: Menu
  },
  {
    path: '/auth/login',
    name: 'Login',
    component: Login,
    meta: {
      hideHeader: true,
      hideFooter: true,
      guestOnly: true
    }
  },
  {
    path: '/auth/register',
    name: 'Register',
    component: Register,
    meta: {
      hideHeader: true,
      guestOnly: true
    }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: {
      requiresAuth: true
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('authToken')
  
  if (to.meta.requiresAuth && !token) {
    return next('/auth/login')
  }
  if (to.meta.guestOnly && token) {
    return next('/profile')
  }
  next()
})

export default router