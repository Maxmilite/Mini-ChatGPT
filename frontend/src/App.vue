<script setup lang="ts">
import { onMounted, ref } from "vue";
import { ElMessage, messageEmits } from 'element-plus'
import { stringify } from "querystring";

const serverAddress = "http://127.0.0.1:5173/api"
const state = ref(0);
const loggedIn = ref(false);
const userName = ref("");

function stateHandler(e: number) {
  state.value = -1;
  setTimeout(() => {
    state.value = e;
    if (e == 1 && !loggedIn.value) {
      state.value = 0;
      ElMessage.error("You need to sign in before using Mini-ChatGPT.")
    }
  }, 10);
}

const sleep = (delay: number) => new Promise((resolve) => setTimeout(resolve, delay));

async function submitMessage(message: string, callback: Function) {
  let returnMessage = "";
  let HTTPRequest = new XMLHttpRequest();
  HTTPRequest.open("GET", serverAddress + "/api/message?message=" + message, true);
  HTTPRequest.onreadystatechange = () => {
    if (HTTPRequest.readyState == 4) {
      if (HTTPRequest.status == 200) {
        returnMessage = HTTPRequest.responseText;
        callback(returnMessage);
      }
      else if (HTTPRequest.status == 401) {
        callback("You need to log in before using this ChatBot.");
      } else {
        callback("An error occurred while corresponding with the chatbot.");
      }
    }
  }
  HTTPRequest.send();
}

function getACList() {
  let returnMessage = "";
  let HTTPRequest = new XMLHttpRequest();
  HTTPRequest.open("GET", serverAddress + "/api/autocomplete", false);
  try {
    HTTPRequest.send();
    returnMessage = HTTPRequest.responseText;
    return JSON.parse(returnMessage);
  } catch (error) {
    return "An error occurred while corresponding with the chatbot."
  }
}

function getHotSpot() {
  let returnMessage = "";
  let HTTPRequest = new XMLHttpRequest();
  HTTPRequest.open("GET", serverAddress + "/api/hotspot", false);
  try {
    HTTPRequest.send();
    returnMessage = HTTPRequest.responseText;
    return JSON.parse(returnMessage);
  } catch (error) {
    return "An error occurred while corresponding with the chatbot."
  }
}

function login(username: string, password: string) {
  let HTTPRequest = new XMLHttpRequest();
  HTTPRequest.open("POST", serverAddress + "/api/login", false);
  HTTPRequest.withCredentials = true;
  HTTPRequest.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  try {
    HTTPRequest.send(JSON.stringify({ "username": username, "password": password }));
    let returnMessage = JSON.parse(HTTPRequest.responseText);
    if (returnMessage.code == 200) {
      ElMessage.success(returnMessage.msg);
      loggedIn.value = true;
      userName.value = getSession();
      return 1;
    } else {
      ElMessage.error("Error: " + returnMessage.msg);
      return 0;
    }
  } catch (error) {
    ElMessage.error("Error: Network Error");
    return 0;
  }
}

function logout() {
  let HTTPRequest = new XMLHttpRequest();
  HTTPRequest.open("GET", serverAddress + "/api/logout", false);
  HTTPRequest.withCredentials = true;
  try {
    HTTPRequest.send();
    let returnMessage = JSON.parse(HTTPRequest.responseText);
    ElMessage.success(returnMessage.msg);
    loggedIn.value = false;
    stateHandler(0);
    return 0;
  } catch (error) {
    ElMessage.error("Error: Network Error");
    return 0;
  }
}

function getSession() {
  let HTTPRequest = new XMLHttpRequest();
  HTTPRequest.open("GET", serverAddress + "/api/session", false);
  HTTPRequest.withCredentials = true;
  try {
    HTTPRequest.send();
    let returnMessage = JSON.parse(HTTPRequest.responseText);
    if (returnMessage.code == 200) {
      return returnMessage.msg;
    } else {
      return "";
    }
  } catch (error) {
    return "";
  }
}

onMounted(() => {
  let res = getSession();
  if (res != "") {
    userName.value = res;
    loggedIn.value = true;
  } else {
    loggedIn.value = false;
  }
});

</script>

<template>
  <el-config-provider namespace="ep">
    <BaseHeader @response="(e) => stateHandler(e)" :username="userName" :login-function="login" :logged-in="loggedIn" :logout-function="logout"/>
    <div style="display: flex">
      <BaseSide @response="(e) => stateHandler(e)" :state="state" :loggedIn="loggedIn" />
      <div style="width: 100%; height: calc(100vh - 60px);">
        <Welcome v-if="state == 0" :logged-in="loggedIn" @response="(e) => stateHandler(e)" msg="Mini ChatGPT" />
        <ChatSession v-else-if="state == 1" :submit-function="submitMessage" :auto-complete-list-function="getACList" />
        <HotSpot v-else-if="state == 2" :hot-spot-function="getHotSpot"></HotSpot>
      </div>
    </div>
  </el-config-provider>
</template>
  
<style>
#app {
  text-align: center;
  color: var(--ep-text-color-primary);
}

.element-plus-logo {
  width: 50%;
}
</style>
