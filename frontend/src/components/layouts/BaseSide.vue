<script lang="ts" setup>
import { nextTick, ref } from 'vue'
import {
  Location,
  Document,
  Menu as IconMenu,
  Setting,
} from '@element-plus/icons-vue'
import { ElButton, ElInput } from 'element-plus';

const props = defineProps({
  state: Number
})

const isCollapse = ref(true)

const inputVisible = ref(false);
const InputRef = ref<InstanceType<typeof ElInput>>();
const inputValue = ref('')

const showInput = () => {
  inputVisible.value = true
  nextTick(() => {
    InputRef.value!.input!.focus()
  })
}

const handleInputConfirm = () => {
  if (inputValue.value) {
    groupList.value.push({
      id: groupList.value.length + 1,
      text: inputValue.value,
      child: []
    });
    // console.log(groupList)
  }
  inputVisible.value = false;
  inputValue.value = "";
}

const SessionItem = { id: 0, text: "Session" }
const GroupItem = { id: 0, text: "Default", child: [ SessionItem ] }

const groupList = ref([
  {
    id: 1, text: "Default", child: [
      { id: 1, text: "Session 1" },
      { id: 2, text: "Session 2" },
      { id: 3, text: "Session 3" },
      { id: 4, text: "Session 4" },
    ]
  },
  {
    id: 2, text: "Default", child: [
      { id: 1, text: "Session 1" },
      { id: 2, text: "Session 2" },
      { id: 3, text: "Session 3" },
      { id: 4, text: "Session 4" },
    ]
  },
  
]);

const handleGroupClose = (key: typeof GroupItem) => {
  groupList.value.splice(groupList.value.indexOf(key), 1);
}

const handleItemClose = (father: typeof GroupItem, key: typeof SessionItem) => {
  father.child.splice(father.child.indexOf(key), 1);
}

</script>

<template>
  <el-menu default-active="2" class="el-menu-vertical-demo" :collapse="isCollapse">
    <el-menu-item index="0" @click="isCollapse = !isCollapse">
      <el-icon v-if="isCollapse">
        <ArrowRightBold />
      </el-icon>
      <el-icon v-else>
        <ArrowLeftBold />
      </el-icon>
      <template #title>Sessions</template>
    </el-menu-item>
    <el-menu-item v-if="state === 1" >
      <el-icon>
        <Document />
      </el-icon>
      <span>Current</span>
    </el-menu-item>
    <el-sub-menu 
      v-for="group in groupList" :allow-drop="true" :allow-drag="true"
      :index="(groupList.indexOf(group) + 1).toString()" draggable="true">
      <template #title>
        <el-icon>
          <MessageBox />
        </el-icon><span>{{ group.text }}</span>
        <el-icon v-if="!isCollapse" style="margin-left: 10px" @click="handleGroupClose(group)">
          <Close />
        </el-icon>
      </template>
      <el-menu-item-group>
        <template #title v-if="isCollapse"><span>{{ group.text }}</span></template>
        <el-menu-item draggable="true" v-for="item in group.child" :index="(groupList.indexOf(group) + 1) + '-' + (group.child.indexOf(item) + 1)">
          <el-icon>
            <Document />
          </el-icon>{{ item.text }}
          <el-icon style="margin-left: 10px" @click="handleItemClose(group, item)">
            <Close />
          </el-icon>
        </el-menu-item>
      </el-menu-item-group>
    </el-sub-menu>

    <div v-if="!isCollapse">
      <el-button v-if="!inputVisible" style="margin-top: 10px;" type="default" size="default" class="w-30"
        @click="showInput">
        + New Group
      </el-button>
      <el-input v-else style="margin-top: 10px;" type="default" size="default" class="w-30" ref="InputRef"
        v-model="inputValue" @keyup.enter="handleInputConfirm" @blur="handleInputConfirm">
      </el-input>
    </div>

  </el-menu>
</template>

