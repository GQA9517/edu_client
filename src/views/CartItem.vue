<template>
  <div class="cart_item" v-show="is_show">
      <div class="cart_column column_1">
        <el-checkbox class="my_el_checkbox" v-model="course.selected" @change="select(course.selected)"></el-checkbox>
      </div>
      <div class="cart_column column_2">
        <img :src="course.course_img" alt="">
        <span><router-link :to="'/detail/'+course.id">{{ course.name }}</router-link></span>
      </div>
      <div class="cart_column column_3">
        <el-select v-model="course.expire_id" size="mini" placeholder="请选择购买有效期" class="my_el_select">
          <el-option :label="item.expire_text" :value="item.id"
                     v-for="(item, index) in course.expire_list" :key="index">
          </el-option>
        </el-select>
      </div>
      <div class="cart_column column_4">¥{{ course.price }}</div>
    <div class="cart_column column_4">
      <el-button type="danger" @click="del_course">删除</el-button>
    </div>
  </div>
</template>
<script>
export default {
  name: "CartItem",
  props: ['course'],
  watch: {
    'course.selected': function () {
      // 后台发起请求改变状态
      this.change_select();
    },
    'course.expire_id': function () {
      this.patch_course()
    }
  },
  data() {
    return {
      checked: 0,
      // expire: 0,
      is_show: true
    }
  },
  methods: {
    //改变选框
    select:function (selected){
      let token = sessionStorage.token
      this.$axios({
        method:'put',
        url:this.$settings.HOST + 'cart/option/',
        headers:{
          "Authorization": "jwt "+ token
        },
        data:{course_id:this.course.id}
      }).then(response=>{
        console.log(response);
        this.$emit('select',response.data.message)
      }).catch(error=>{
        console.log(error);
      })
    },
    //删除
    del_course() {
      let token = localStorage.token || sessionStorage.token;
      console.log(token);
      this.$axios({
        url: this.$settings.HOST + "cart/option/",
        method: "delete",
        headers: {
          "Authorization": "jwt " + token,
        },
        data: {
          course_id: this.course.id,
        },
      }).then(res => {
        console.log(res);
        this.$message.success("删除成功！")
        this.is_show = false
      }).catch(error => {
        console.log(error);
      })
    },
    //更新
    patch_course() {
      console.log(this.course.expire_id);
      let token = localStorage.token || sessionStorage.token
      this.$axios.patch(this.$settings.HOST + "cart/option/", {
        course_id: this.course.id,
        expire: this.course.expire_id
      }, {
        headers: {
          "Authorization": "jwt " + token
        },
      }).then(res => {
        this.$emit("expire", res.data.message)
      }).catch(error => {
        console.log(error);
      })
    },
    change_select() {
      this.$message.success("更新成功")
    }
  }
}
</script>

<style scoped>
.cart_item::after {
  content: "";
  display: block;
  clear: both;
}

.cart_column {
  float: left;
  height: 250px;
}

.cart_item .column_1 {
  width: 88px;
  position: relative;
}

.my_el_checkbox {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  top: 0;
  margin: auto;
  width: 16px;
  height: 16px;
}

.cart_item .column_2 {
  padding: 67px 10px;
  width: 520px;
  height: 116px;
}

.cart_item .column_2 img {
  width: 175px;
  height: 115px;
  margin-right: 35px;
  vertical-align: middle;
}

.cart_item .column_3 {
  width: 197px;
  position: relative;
  padding-left: 10px;
}

.my_el_select {
  width: 117px;
  height: 28px;
  position: absolute;
  top: 0;
  bottom: 0;
  margin: auto;
}

.cart_item .column_4 {
  padding: 67px 10px;
  height: 116px;
  width: 142px;
  line-height: 116px;
}

</style>