import version389 from '../api/moodle-3.8.9.json'

export default [
  {
    path: '/',
    redirect: '3-8-9'
  },
  {
    path: '/:version',
    name: 'api',
    component: () => import('../views/ApiView.vue'),
    props: (route) => ({
      api: version389,
      root: '3-8-9'
    })
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue')
  }
]
