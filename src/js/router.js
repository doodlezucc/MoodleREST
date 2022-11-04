import version389 from '../api/moodle-3.8.9.json'
import version400 from '../api/moodle-4.0.0.json'

export default [
  {
    path: '/',
    redirect: '4-0-0'
  },
  {
    path: '/:version',
    name: 'api',
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
