<script lang="ts" setup>
import { ElMessage } from 'element-plus';
import { reactive, ref } from 'vue';
import { toggleDark } from '~/composables';

const emit = defineEmits(['response']);
const dialogFormVisible = ref(false);
const form = reactive({
  name: '',
  password: ''
})
const formLabelWidth = '100px';


function exit(e: number) {
  emit('response', e);
}

const props = defineProps({
  loggedIn: Boolean,
  loginFunction: Function,
  logoutFunction: Function
});

const login = () => {
  let username = form.name;
  let password = form.password;
  let response = props.loginFunction!(username, password);
  if (!response) {
    return;
  }
  dialogFormVisible.value = false;
}

const logout = () => {
  props.logoutFunction!();
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
        <el-menu-item @click="exit(2)" index="5-1">Hotspot</el-menu-item>
      </el-menu-item-group>
    </el-sub-menu>
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
      <el-menu-item index="6-1"><el-icon>
          <InfoFilled />
        </el-icon>Info</el-menu-item>
      <el-menu-item index="6-2" v-if="loggedIn" @click="logout()"><el-icon>
          <Close />
        </el-icon>Logout</el-menu-item>
      <el-menu-item index="6-3" v-else @click="dialogFormVisible = true"><el-icon>
          <Avatar />
        </el-icon>Log In</el-menu-item>
    </el-sub-menu>
  </el-menu>
  <el-dialog draggable destroy-on-close v-model="dialogFormVisible" title="Log In" :center="true"
    width="calc(max(500px, 30%))">
    <el-form :model="form" style="display: flex; flex-direction: column; align-items: center;">
      <el-form-item label="User Name" :label-width="formLabelWidth">
        <el-input style="width: 300px; margin-left: 0; margin-right: 0" v-model="form.name" autocomplete="off" />
      </el-form-item>
      <el-form-item label="Password" :label-width="formLabelWidth">
        <el-input style="width: 300px; margin-left: 0; margin-right: 0" type="password" v-model="form.password"
          autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <p>If you have not signed in before, you will be automatically registered.</p>
      <span class="dialog-footer">
        <el-button @click="() => { dialogFormVisible = false; }">Cancel</el-button>
        <el-button type="primary" @click="login()">
          Confirm
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<style>
.flex-grow {
  flex-grow: 1;
}

.el-button--text {
  margin-right: 15px;
}

.dialog-footer button:first-child {
  margin-right: 10px;
}
</style>