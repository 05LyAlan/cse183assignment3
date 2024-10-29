"use strict";

// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {
    data() {
      return {
        newItemName: '',
        items: []
      };
    },
    methods: {
      loadData() {
        axios.get(load_data_url).then(response => {
          this.items = response.data.items;
        });
      },
      addItem() {
        if (this.newItemName.trim() === '') return;
        axios.post(add_item_url, { item_name: this.newItemName }).then(response => {
          this.items.unshift(response.data.item);
          this.newItemName = '';
        });
      },
      updateItem(item) {
        axios.post(update_item_url, { id: item.id, purchased: item.purchased }).then(() => {
          this.sortItems();
        });
      },
      deleteItem(item) {
        axios.post(delete_item_url, { id: item.id }).then(response => {
          if (response.data.status === "ok") {
            this.items = this.items.filter(i => i.id !== item.id); // Remove item locally
          } else {
            console.error("Failed to delete item from backend.");
          }
        }).catch(error => {
          console.error("Error deleting item:", error);
        });
      },
      sortItems() {
        this.items.sort((a, b) => a.purchased - b.purchased || b.id - a.id);
      }
    },
    mounted() {
      this.loadData();
    }
  };
  
  Vue.createApp(app).mount("#app");