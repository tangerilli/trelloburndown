var Sprint = Backbone.Model.extend({
    urlRoot: "/sprints"
});
var Sprints = Backbone.Collection.extend({
    model: Sprint,
    url: "/sprints",
});

var SprintView = Backbone.View.extend({
    tagName: "div",
    className: "sprint",
    initialize: function() {
        this.template = Handlebars.compile($("#sprint-template").html());
        this.model.bind("change", this.render, this);
    },
    events: {
        "blur input.hover_edit":"edit_field"
    },
    render: function() {
        var html = this.template(this.model.toJSON());
        this.$el.html(html);
        return this;
    },
    edit_field: function(ev) {
        var field_name = $(ev.target).attr("name");
        var attr = {};
        attr[field_name] = $(ev.target).val();
        this.model.set(attr);
        this.model.save();
    }
});

var SprintListItemView = Backbone.View.extend({
    tagName: "li",
    className: "sprint",
    initialize: function() {
        this.template = Handlebars.compile($("#sprint-item-template").html());
        this.model.bind("change", this.render, this);
    },
    events: {
        "click i.delete_sprint":"remove_sprint"
    },
    render: function() {
        var data = this.model.toJSON();
        data.url = this.model.url();
        var html = this.template(data);
        this.$el.html(html);
        return this;
    },
    remove_sprint: function() {
        this.model.destroy();
    }
})

var SprintsView = Backbone.View.extend({
    tagName: "div",
    id: "sprints_view",
    initialize: function() {
        this.template = Handlebars.compile($("#sprints-template").html());
        this.collection.bind("add", this.render, this);
        this.collection.bind("remove", this.render, this);
    },
    events: {
        "click #add_new_sprint":"add_sprint"
    },
    render: function() {
        var html = this.template();
        this.$el.html(html);
        var sprint_list = this.$("#sprint_list");
        this.collection.each(function(sprint) {
            var view = new SprintListItemView({model: sprint});
            sprint_list.append(view.render().el);
        });
        return this;
    },
    add_sprint: function() {
        var sprint_name = this.$("#new_sprint").val();
        if(sprint_name) {
            var sprint = new Sprint({
                name: sprint_name,
            });
            this.collection.add(sprint);
            sprint.save();
            this.$("#new_sprint").val("")
        }
        return false;
    }
});

var BurndownRouter = Backbone.Router.extend({
    routes: {
        "":"sprints",
        "sprints":"sprints",
        "sprints/:id":"sprint"
    },
    initialize: function() {
        this._current_view = null;
    },
    sprints: function() {
        console.debug("sprints!");
        this.clear_views();
        var sprints = new Sprints;
        var router = this;
        sprints.fetch({
            success: function() {
                var sprints_view = new SprintsView({
                    collection: sprints,
                });
                router._current_view = sprints_view;
                $("div#main").html(sprints_view.render().el);
            }
        })
    },
    sprint: function(id) {
        console.debug("viewing sprint");
        this.clear_views();
        var sprint = new Sprint({id: id});
        var router = this;
        sprint.fetch({
            success: function() {
                var view = new SprintView({
                    model: sprint
                });
                console.debug(sprint);
                router._current_view = view;
                $("div#main").html(view.render().el);
                
                Morris.Line({
                    element: "burndown_chart",
                    data: sprint.get("efforts"),
                    xkey: "timestamp",
                    ykeys: ["remaining", "ideal"],
                    labels: ["Remaining", "Ideal"],
                    hideHover: true
                });
            }
        });
    },
    clear_views: function() {
        if(this._current_view != null)
        {
            this._current_view.remove();
        }
    }
});