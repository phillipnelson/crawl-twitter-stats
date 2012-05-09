
d3.json(DATA_FILE, function(json) {
	var matrix = new Array();
	var users = new Array();

	json.forEach(function(user) {
		users.push(user.username);
	});

	json.forEach(function(user) {
		var row = new Array();
		var relations_total = 0;

		for (var i in user.relations) {
			relations_total += user.relations[i];
		}

		json.forEach(function(user1) {
            multiplier = relations_total > 0 ? user.influence/relations_total : 0;
			row.push(user1.id in user.relations ? user.relations[user1.id] * multiplier : 0);
		});
		matrix.push(row);
	});


    var chord = d3.layout.chord()
        .padding(.05)
        .sortSubgroups(d3.descending)
        .matrix(matrix);

    var width = 1000,
        height = 800,
        innerRadius = Math.min(width, height) * .41,
        outerRadius = innerRadius * 1.1;

    var fill = d3.scale.ordinal()
        .domain(d3.range(6))
        .range(["#DADAEB","#BCBDDC","#9E9AC8","#807DBA","#6A51A3","#4A1486"]);

    var svg = d3.select("#chart")
      .append("svg")
        .attr("width", width)
        .attr("height", height)
      .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    var g = svg.selectAll("g.group")
            .data(chord.groups)
          .enter().append("svg:g")
            .attr("class", "group");

    g.append("path")
        .style("fill", function(d) { return fill(d.index); })
        .style("stroke", function(d) { return fill(d.index); })
        .attr("d", d3.svg.arc().innerRadius(innerRadius).outerRadius(outerRadius))
        .attr("id", function(d, i) { return "group-" + d.index; })
        .on("mouseover", fade(.1))
        .on("mouseout", fade(1));
  
    g.append("svg:text")
        .attr("x", 6)
        .attr("dy", 15)
        .filter(function(d) { return d.value > 1; })
      .append("svg:textPath")
        .attr("xlink:href", function(d) { return "#group-" + d.index; })
        .text(function(d) { return users[d.index]; });


    var ticks = svg.append("g")
      .selectAll("g")
        .data(chord.groups)
      .enter().append("g")
      .selectAll("g")
        .data(groupTicks)
      .enter().append("g")
        .attr("transform", function(d) {
          return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")"
              + "translate(" + outerRadius + ",0)";
        });

    ticks.append("line")
        .attr("x1", 1)
        .attr("y1", 0)
        .attr("x2", 5)
        .attr("y2", 0)
        .style("stroke", "#ddd");

    ticks.append("text")
        .attr("x", 8)
        .attr("dy", ".35em")
        .attr("text-anchor", function(d) {
          return d.angle > Math.PI ? "end" : null;
        })
        .attr("transform", function(d) {
          return d.angle > Math.PI ? "rotate(180)translate(-16)" : null;
        })
        .text(function(d) { return d.label; })
        .style("stroke", "#ddd");;

    svg.append("g")
        .attr("class", "chord")
      .selectAll("path")
        .data(chord.chords)
      .enter().append("path")
        .style("fill", function(d) { return fill(d.target.index); })
        .attr("d", d3.svg.chord().radius(innerRadius))
        .style("opacity", 1);

    /** Returns an array of tick angles and labels, given a group. */
    function groupTicks(d) {
      var k = (d.endAngle - d.startAngle) / d.value;
      return d3.range(0, d.value, 10).map(function(v, i) {
        return {
          angle: v * k + d.startAngle,
          label: i % 5 ? null : v / 10 + ""
        };
      });
    }

    /** Returns an event handler for fading a given chord group. */
    function fade(opacity) {
      return function(g, i) {
        svg.selectAll("g.chord path")
            .filter(function(d) {
              return d.source.index != i && d.target.index != i;
            })
          .transition()
            .style("opacity", opacity);
      };
    }
    
});
