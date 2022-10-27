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
      api: {
        version: "3.420 haha :D"
      }
    })
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue')
  }
]
