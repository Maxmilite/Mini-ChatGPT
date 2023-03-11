<script setup lang="ts">;
import { ref } from "vue";
import { ElMessage } from 'element-plus';

const props = defineProps({
  msg: String,
  loggedIn: Boolean
});

const emit = defineEmits(['response']);

const startSession = () => {
  emit('response', 1);
}

</script>

<template>
  <div style="padding-top: 60px">
    <h1>{{ msg }}</h1>

  <p>
    A chat window that can help you solve problems.
  </p>

  <!-- example components -->
  <div class="my-2 text-center flex flex-wrap justify-center items-center"
    style="padding-top: 35vh">
    <!-- <el-button @click="count++">count is: {{ count }}</el-button> -->
    <el-button v-if="loggedIn" type="primary" plain size="large" @click="startSession()">
      Try it now
      <el-icon class="el-icon"><ArrowRight /></el-icon>
    </el-button>
    <p v-else>You need to sign in before using Mini-ChatGPT.</p>
    <!-- <el-button type="success" @click="count++">count is: {{ count }}</el-button>
    <el-button type="warning" @click="count++">count is: {{ count }}</el-button>
    <el-button type="danger" @click="count++">count is: {{ count }}</el-button>
      <el-button type="info" @click="count++">count is: {{ count }}</el-button> -->
    </div>

    <!-- 

    <div>
      <el-tag type="success" class="m-1">Tag 1</el-tag>
      <el-tag type="warning" class="m-1">Tag 1</el-tag>
      <el-tag type="danger" class="m-1">Tag 1</el-tag>
      <el-tag type="info" class="m-1">Tag 1</el-tag>
    </div>

    <div class="my-2">
      <el-input class="m-2" v-model="input" style="width: 200px;" />
      <el-date-picker class="m-2" v-model="curDate" type="date" placeholder="Pick a day"></el-date-picker>
    </div> -->
  </div>
</template>

<style>
.ep-button {
  margin: 4px;
}

.ep-button+.ep-button {
  margin-left: 0;
  margin: 4px;
}
</style>
