<template>
  <div class="footer">
    <ul>
      <li v-for="(banner, index) in nav_list" :key="index">
        {{banner.title}}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "Footer",
  data() {
    return {
      nav_list: [],
    }
  },
  methods: {
    get_all_banner() {
      this.$axios({
        url: this.$settings.HOST + "home/nav/",
        method: 'get',
      }).then(res => {
        let list1=[]
        for (let i = 0; i < res.data.length; i++) {
          if (res.data[i].is_position===2){
            list1.push(res.data[i])
          }
        }
        this.nav_list = list1;
        console.log(32, res.data)
      }).catch(error => {
        console.log(error);
      })
    },
  },
  created() {
    this.get_all_banner()
  },
}
</script>

<style scoped>

.footer {
  width: 100%;
  height: 128px;
  background: #25292e;
  color: #fff;
}

.footer ul {
  margin: 0 auto 16px;
  padding-top: 38px;
  width: 810px;
}

.footer ul li {
  float: left;
  width: 112px;
  margin: 0 10px;
  text-align: center;
  font-size: 14px;
}

.footer ul::after {
  content: "";
  display: block;
  clear: both;
}

.footer p {
  text-align: center;
  font-size: 12px;
}
</style>