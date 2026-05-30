// import { ref } from 'vue'
// import axios from 'axios'

// export function useAnimatronics() {
//   const animatronics = ref([])
//   const loading = ref(true)
//   const error = ref(null)

//   const fetchAnimatronics = async () => {
//     try {
//       const response = await axios.get('http://localhost:5000/api/animatronics')
      
//       if (response.data?.success && Array.isArray(response.data.data)) {
//         // 🔥 НОРМАЛИЗАЦИЯ ДАННЫХ
//         // Мы приводим ответ сервера к единому стандарту, чтобы компонент всегда работал
//         animatronics.value = response.data.data.map(item => ({
//           ...item, // Сохраняем все исходные поля
          
//           // 1. Картинка: пробуем разные варианты названий полей
//           image: item.image || item.image_url || item.img || 'https://via.placeholder.com/300?text=No+Image',
          
//           // 2. Имя: если нет name, берем title
//           name: item.name || item.title,
//           title: item.title || item.name,
          
//           // 3. Маршрут: если сервер не прислал route, генерируем его сами по ID
//           route: item.route || `/character/${item.id}`
//         }))
        
//       } else {
//         error.value = 'Сервер вернул некорректные данные'
//       }
//     } catch (err) {
//       error.value = err.response?.data?.message || err.message || 'Ошибка соединения с сервером'
//       console.error('Ошибка загрузки аниматроников:', err)
//     } finally {
//       loading.value = false
//     }
//   }

//   fetchAnimatronics()

//   return {
//     animatronics,
//     loading,
//     error,
//     fetchAnimatronics
//   }
// }


import { ref } from 'vue'
import axios from 'axios'

export function useAnimatronics() {
  const animatronics = ref([])
  const loading = ref(true)
  const error = ref(null)

  const fetchAnimatronics = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/animatronics')
      
      if (response.data?.success && Array.isArray(response.data.data)) {
        // 🔥 НОРМАЛИЗАЦИЯ ДАННЫХ
        animatronics.value = response.data.data.map(item => {
          // Получаем route из бэкенда или генерируем свой
          let route = item.route || `/character/${item.id}`
          
          // 🔥 ЗАМЕНА: если бэкенд шлёт /animatronic/... → меняем на /character/...
          if (route && route.startsWith('/animatronic/')) {
            route = route.replace('/animatronic/', '/character/')
          }
          
          return {
            ...item,
            image: item.image || item.image_url || item.img || 'https://via.placeholder.com/300?text=No+Image',
            name: item.name || item.title,
            title: item.title || item.name,
            route: route // 👈 Возвращаем исправленный путь
          }
        })
        
      } else {
        error.value = 'Сервер вернул некорректные данные'
      }
    } catch (err) {
      error.value = err.response?.data?.message || err.message || 'Ошибка соединения с сервером'
      console.error('Ошибка загрузки аниматроников:', err)
    } finally {
      loading.value = false
    }
  }

  fetchAnimatronics()

  return {
    animatronics,
    loading,
    error,
    fetchAnimatronics
  }
}