import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth' 
import { createPinia } from 'pinia'
import Home from '../views/Home.vue'
import AboutUs from '../views/AboutUs.vue'
import Stars from '../views/Stars.vue'
import Merch from '../views/Merch.vue'
import Cast from '../views/Cast.vue'
import Menu from '../views/Menu.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Profile from '../views/Profile.vue'
import Orders from '../views/Orders.vue'
import Admin from '../views/Admin.vue'
import Cart from '../views/Cart.vue'
import ProductPage from '../views/ProductPage.vue'
import Recover from '../views/Recover.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/about-us', name: 'AboutUs', component: AboutUs },
  { path: '/stars', name: 'Stars', component: Stars },
  { path: '/merch', name: 'Merch', component: Merch },
  { path: '/cast', name: 'Cast', component: Cast },
  { path: '/menu', name: 'Menu', component: Menu },
  {
    path: '/auth/login',
    name: 'Login',
    component: Login,
    meta: { hideHeader: true, guestOnly: true }
  },
  {
    path: '/auth/register',
    name: 'Register',
    component: Register,
    meta: { hideHeader: true, guestOnly: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile/orders',
    name: 'Orders',
    component: Orders,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile/cart',              
    name: 'Cart',                       
    component: () => import('@/views/Cart.vue'),  
    meta: { requiresAuth: true }        
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/product/:id',
    name: 'ProductPage',
    component: ProductPage,
    props: true
  },

  {
    path: '/character/:id',
    name: 'CharacterPage',
    component: () => import('../views/CharacterPage.vue'),
    props: true
  },

  {
  path: '/cast/:id',
  name: 'CastDetail',
  component: () => import('../views/CharacterPage.vue'), 
  props: true
},

  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue')
  },
  {
  path: '/auth/recovery',
  name: 'Recover',
  component: () => import('@/views/Recover.vue'),
  meta: { 
    hideHeader: true, 
    hideFooter: true,
    requiresAuth: false
  }
}
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return { top: 0, left: 0 }
  }
})

router.beforeEach((to, from, next) => {
  const rawToken = localStorage.getItem('authToken')
  const rawUser = localStorage.getItem('user')
  
  if (rawToken && rawUser) {
    const auth = useAuthStore()
    if (!auth.token) {
      auth.token = rawToken
      auth.user = JSON.parse(rawUser)
    }
  }
  
  if (to.meta.requiresAuth && !rawToken) {
    return next({ path: '/auth/login', query: { redirect: to.fullPath } })
  }
  
  if (to.meta.guestOnly && rawToken) {
    return next({ path: '/profile' })
  }
  
  if (to.meta.requiresAdmin) {
    try {
      const user = rawUser ? JSON.parse(rawUser) : null
      if (!user || user.role !== 'admin') {
        return next({ path: rawToken ? '/profile' : '/auth/login' })
      }
    } catch {
      return next({ path: '/auth/login' })
    }
  }
  
  next()
})

export default router