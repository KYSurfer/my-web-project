<template>
  <main class="admin-page">
    <h1 class="page-title">Админ-панель</h1>
    
    <div v-if="loading" class="state-message">
      <div class="spinner"></div>
      <p>Загрузка...</p>
    </div>
    
    <div v-else-if="error" class="state-message error">
      <p>{{ error }}</p>
      <button @click="fetchProducts" class="retry-btn">Повторить</button>
    </div>
    
    <div v-else-if="!isAdmin" class="state-message error">
      <p>Доступ только для администраторов</p>
      <router-link to="/" class="retry-btn">На главную</router-link>
    </div>
    
    <div v-else class="admin-content">
      <section class="admin-stats">
        <div class="stat-card">
          <span class="stat-num">{{ products.length }}</span>
          <span class="stat-label">Товаров</span>
        </div>
        <div class="stat-card">
          <span class="stat-num">{{ foodCount }}</span>
          <span class="stat-label">Еда</span>
        </div>
        <div class="stat-card">
          <span class="stat-num">{{ merchCount }}</span>
          <span class="stat-label">Мерч</span>
        </div>
        <div class="stat-card">
          <span class="stat-num">{{ users.length }}</span>
          <span class="stat-label">Пользователей</span>
        </div>
      </section>
      <section class="admin-list-section users-section">
        <h2>Пользователи</h2>
        <div class="users-table">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Имя</th>
                <th>Email</th>
                <th>Роль</th>
                <th>Дата регистрации</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td>{{ user.id }}</td>
                <td>{{ user.username }}</td>
                <td>{{ user.email }}</td>
                <td>
                  <span class="role-badge" :class="user.role">
                    {{ user.role === 'admin' ? 'Админ' : 'Пользователь' }}
                  </span>
                </td>
                <td>{{ formatDate(user.created_at) }}</td>
                <td>
                  <button 
                    @click="deleteUser(user.id)" 
                    class="btn-delete"
                    :disabled="user.role === 'admin' && user.id === currentAdminId"
                    :title="user.role === 'admin' && user.id === currentAdminId ? 'Нельзя удалить себя' : 'Удалить пользователя'"
                  >
                    🗑️
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-if="users.length === 0" class="empty-message">Нет зарегистрированных пользователей</p>
      </section>

      <section class="admin-form-section">
        <h2>Добавить новый товар</h2>
        <form @submit.prevent="submitProduct" class="admin-form">
          <div class="form-row">
            <div class="form-group">
              <label>Название *</label>
              <input v-model="form.name" type="text" required placeholder="Например: Бон-Бургер">
            </div>
            <div class="form-group">
              <label>Цена (₽) *</label>
              <input v-model.number="form.price" type="number" min="0" step="0.01" required>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Категория *</label>
              <input v-model="form.category" type="text" required placeholder="Бургеры, Одежда, и т.д.">
            </div>
            <div class="form-group">
              <label>Остаток на складе *</label>
              <input v-model.number="form.stock" type="number" min="0" required>
            </div>
          </div>
          <div class="form-group">
            <label>URL изображения *</label>
            <input v-model="form.image_url" type="url" required placeholder="http://localhost:5000/static/images/...">
          </div>
          <div class="form-group">
            <label>Описание</label>
            <textarea v-model="form.description" rows="3" placeholder="Краткое описание товара"></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Тип товара *</label>
              <select v-model="form.is_food" required>
                <option :value="true">Еда (Меню)</option>
                <option :value="false">Мерч (Товары)</option>
              </select>
            </div>
          </div>
          <button type="submit" :disabled="submitting" class="btn-submit">
            {{ submitting ? 'Добавление...' : '► Добавить товар' }}
          </button>
          <p v-if="formError" class="form-error">{{ formError }}</p>
          <p v-if="formSuccess" class="form-success">{{ formSuccess }}</p>
        </form>
      </section>

      <section class="admin-list-section">
        <h2>Все товары</h2>
        <div class="products-table">
          <table>
            <thead>
              <tr>
                <th>Изображение</th>
                <th>Название</th>
                <th>Категория</th>
                <th>Цена</th>
                <th>Тип</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in products" :key="item.id">
                <td><img :src="item.image_url" :alt="item.name" class="table-img"></td>
                <td>{{ item.name }}</td>
                <td>{{ item.category }}</td>
                <td>{{ item.price }} ₽</td>
                <td>
                  <span class="type-badge" :class="item.is_food ? 'food' : 'merch'">
                    {{ item.is_food ? 'Еда' : 'Мерч' }}
                  </span>
                </td>
                <td>
                  <button @click="deleteProduct(item.id)" class="btn-delete">🗑️</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  </main>
</template>

<script>
import api from '@/plugins/axios'

export default {
  name: 'Admin',
  data() {
    return {
      products: [],
      users: [], 
      loading: true,
      error: null,
      isAdmin: false,
      currentAdminId: null,
      form: {
        name: '',
        price: 0,
        image_url: '',
        description: '',
        is_food: true,
        category: '',
        stock: 0
      },
      submitting: false,
      formError: null,
      formSuccess: null
    }
  },
  computed: {
    foodCount() {
      return this.products.filter(p => p.is_food).length
    },
    merchCount() {
      return this.products.filter(p => !p.is_food).length
    }
  },
  async mounted() {
    await this.checkAdmin()
    if (this.isAdmin) {
      await Promise.all([
        this.fetchProducts(),
        this.fetchUsers()
      ])
    }
  },
  methods: {
    async checkAdmin() {
      const token = localStorage.getItem('authToken')
      const user = JSON.parse(localStorage.getItem('user') || '{}')
      
      if (!token || user.role !== 'admin') {
        this.isAdmin = false
        this.loading = false
        return
      }
      this.isAdmin = true
      this.currentAdminId = user.id 
    },
    
    async fetchProducts() {
      try {
        this.loading = true
        const res = await api.get('/admin/products')
        if (res.data?.success) {
          this.products = res.data.data
        }
      } catch (e) {
        this.error = 'Не удалось загрузить товары'
        console.error(e)
      } finally {
        this.loading = false
      }
    },
    
    async fetchUsers() {
      try {
        const res = await api.get('/admin/users')
        if (res.data?.success) {
          this.users = res.data.data
        }
      } catch (e) {
        console.error('Ошибка загрузки пользователей:', e)
      }
    },
    
    async deleteUser(userId) {
      if (userId === this.currentAdminId) {
        alert('❌ Нельзя удалить самого себя!')
        return
      }
      
      const user = this.users.find(u => u.id === userId)
      if (!confirm(`Удалить пользователя "${user?.username || userId}"?`)) return
      
      try {
        const res = await api.delete(`/admin/users/${userId}`)
        if (res.data?.success) {
          this.users = this.users.filter(u => u.id !== userId)
          alert(' Пользователь удалён')
        }
      } catch (e) {
        console.error('Ошибка при удалении:', e)
        alert(' Ошибка: ' + (e.response?.data?.error || 'Не удалось удалить'))
      }
    },
    
    async submitProduct() {
      this.submitting = true
      this.formError = null
      this.formSuccess = null
      
      try {
        const res = await api.post('/admin/products', this.form)
        if (res.data?.success) {
          this.formSuccess = 'Товар добавлен!'
          this.form = { name: '', price: 0, image_url: '', description: '', is_food: true, category: '', stock: 0 }
          await this.fetchProducts()
        }
      } catch (e) {
        this.formError = e.response?.data?.error || 'Ошибка при добавлении'
      } finally {
        this.submitting = false
      }
    },
    
    async deleteProduct(id) {
      if (!confirm('Удалить этот товар?')) return
      try {
        const res = await api.delete(`/admin/products/${id}`)
        if (res.data?.success) {
          this.products = this.products.filter(p => p.id !== id)
        }
      } catch (e) {
        alert('Ошибка при удалении')
      }
    },
    
    formatDate(dateString) {
      if (!dateString) return '—'
      const date = new Date(dateString)
      return date.toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped src="@/assets/styles/views/Admin.css">

</style>