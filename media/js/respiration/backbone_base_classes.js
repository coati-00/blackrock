var BaseModel = Backbone.Model.extend({

	url: function() {
       var url = this.urlRoot;
       if (this.get('id') !== undefined) {
           url += this.get('id') + '/';
       }
       return url;
   }

});


var BaseCollection = Backbone.Collection.extend({

    url: function() {
        var url = this.urlRoot;
        return url;
    }

});


var BaseItemView = Backbone.View.extend({

	render: function () 
    {
        var html = this.template(this.model.toJSON());
        this.$el.html(html);
        return this;
    }

});


var BaseListView = Backbone.View.extend({

    renderCollection: function() {
        this.collection.each(function(model)
        {
            this.$el.append(new this.item_view({
                model: model
            }).render().el);
        }, this);
        return this;
    },
    
    addItem: function(model, collection, options)
    {
        this.$el.append(new this.item_view({
            model: model
        }).render().el);
    }

});



var DeletableItemView = BaseItemView.extend({

    removeItem: function ()
    {   
        this.model.destroy();
    }

});