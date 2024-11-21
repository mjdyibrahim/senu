<template>
  <div>
    <nav>
      <ul>
        <li><NuxtLink to="/">Home</NuxtLink></li>
        <li><NuxtLink to="/about">About</NuxtLink></li>
        <li><NuxtLink to="/contact">Contact</NuxtLink></li>
        <!-- Add more pages as needed -->
      </ul>
    </nav>
    <NuxtRouteAnnouncer />
    <NuxtWelcome />
    <NuxtPage />
  </div>
</template>
