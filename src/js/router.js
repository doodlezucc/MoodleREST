// import version389 from '../api/moodle-3.8.9.json'
import version400 from '../api/moodle-4.0.0.json'

export default [
  {
    path: '/',
    component: () => import('../views/ApiView.vue'),
    props: (route) => ({
      api: version400
    })
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue')
  }
]
