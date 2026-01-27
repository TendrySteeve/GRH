import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    redirect: "/login",
  },
  {
    path: "/login",
    name: "login",
    component: () => import("../views/Login.vue"),
    meta: { requiresAuth: false },
  },
  {
    path: "/register",
    name: "register",
    component: () => import("../views/Register.vue"),
    meta: { requiresAuth: false },
  },
  {
    path: "/schedule",
    name: "schedule",
    component: () => import("../views/Schedule.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/manage-schedule",
    name: "manage-schedule",
    component: () => import("../views/ScheduleManagement.vue"),
    meta: {requiresAuth: true}
  },
  {
    path: "/manage-leave",
    name: "manage-leave",
    component: () => import("../views/LeaveManagement.vue"),
    meta: {requiresAuth: true}
  },
  {
    path: "/setting",
    name: "setting",
    component: () => import("../views/Settings.vue"),
    meta: {requiresAuth: true}
  },

  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: () => import("../views/NotFound.vue"),
  },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("access_token");

  if (to.meta.requiresAuth && !token) {
    next("/login");
  } else if ((to.path === "/login" || to.path === "/register") && token) {
    next("/schedule");
  } else {
    next();
  }
});
