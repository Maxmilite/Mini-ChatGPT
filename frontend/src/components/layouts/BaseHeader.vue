<script lang="ts" setup>
import { toggleDark } from '~/composables';

const emit = defineEmits(['response']);

function exit(e: number) {
  emit('response', e);
}

</script>

<template>
  <el-menu class="el-menu-demo" mode="horizontal" :ellipsis="false">
    <el-menu-item index="1" @click="exit(0)">Mini ChatGPT</el-menu-item>
    <el-sub-menu index="2">
      <template #title>
        <!-- <el-icon> <ChatLineSquare /> </el-icon> -->
        <el-icon>
          <ChatLineSquare />
        </el-icon>Chats
      </template>
      <el-menu-item index="2-1" @click="exit(1)">Start a new chat</el-menu-item>
    </el-sub-menu>
    <el-menu-item index="3" disabled>
      <el-icon>
        <setting />
      </el-icon>Settings
    </el-menu-item>
    <el-sub-menu index="4">
      <template #title>
        <el-icon>
          <Menu />
        </el-icon>
        <span>Utilities</span>
      </template>
    <el-menu-item-group>
      <template #title><span>History</span></template>
      <el-menu-item index="4-1">Latest History</el-menu-item>
      <el-menu-item index="4-2">Find History Message</el-menu-item>
      </el-menu-item-group>
      <el-menu-item-group>
        <template #title><span>Hotspot</span></template>
        <el-menu-item index="5-1">Find Hotspot</el-menu-item>
      </el-menu-item-group>
    </el-sub-menu>
    <!-- <el-menu-item h="full" @click="toggleDark()">
          <button class="border-none w-full bg-transparent cursor-pointer" style="height: var(--ep-menu-item-height);">
            <i inline-flex i="dark:ep-moon ep-sunny" />
          </button>
        </el-menu-item> -->
    <!-- <div class="flex-grow" /> -->
    <div style="flex-grow: 1" />
    <el-menu-item index="5" @click="toggleDark()">
      <button class="border-none bg-transparent cursor-pointer" style="height: var(--ep-menu-item-height);">
        <i inline-flex i="dark:ep-moon ep-sunny" />
      </button>
    </el-menu-item>
    <el-sub-menu index="6">
      <template #title><el-icon>
          <User />
        </el-icon></template>
      <el-menu-item index="6-1"><el-icon><InfoFilled /></el-icon>Info</el-menu-item>
      <el-menu-item index="6-2"><el-icon><Close /></el-icon>Logout</el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>

<style>
.flex-grow {
  flex-grow: 1;
}</style>