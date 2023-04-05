const { createApp } = Vue;
const app = createApp({
	data() {
		return {
			spaces: [],
			selectedSpace: {},
			users: [{ id: "", email: " --- " }],
			selectedUserId: "",
			tools: [],
			tool_ids: [],
			spaceUnits: [],
			selectedUnit: "0",
			fromTimeRange: [],
			fromTime: "",
			toTimeRange: [{ value: "", text: " إلى " }],
			toTime: "",
			attendance_num: 0,
			description: "",
			min_age: 0,
			max_age: 0,
			price_table: [],
			dates: [],
			payment_status: "no_payment",
			isDatepickerShow: false
		};
	},
	computed: {},
	watch: {
		tool_ids(newVal, oldVal) {
			if (newVal.length !== oldVal.length) {
				this.calculate();
			}
		},
		selectedUserId(newVal, oldVal) {
			this.spaces = [];
			this.selectedSpace = {};
			this.getSpaces(newVal);
		},
		selectedSpace() {
			this.fromTime = "";
			this.toTime = "";
			this.price_table = [];
			this.tools = [];
		},
		selectedUnit() {
			this.getReservedDays();
			this.price_table = []
			this.fromTime = "";
			this.toTime = "";
			$("#datepicker").datepicker("destroy");
		},
		attendance_num(newVal, oldVal) {
			if (newVal < 0 || newVal === "") {
				this.attendance_num = 0;
			} else if (newVal % 1 !== 0) {
				this.attendance_num = oldVal;
			}
		},
		min_age(newVal, oldVal) {
			if (newVal < 0 || newVal === "") {
				this.min_age = 0;
			} else if (newVal % 1 !== 0) {
				this.min_age = oldVal;
			}
		},
		max_age(newVal, oldVal) {
			if (newVal < 0 || newVal === "") {
				this.max_age = 0;
			} else if (newVal % 1 !== 0) {
				this.max_age = oldVal;
			}
		},
		toTime(newVal, oldVal) {
			if (oldVal !== newVal) {
				this.getReservedDays();
			}
		}
	},
	mounted() {
		this.getUsers();
	},
	methods: {
		getSpaces(user_id) {
			if (!user_id) {
				return;
			}
			fetch(`/api/spaces?user_id=${user_id}`)
				.then((response) => response.json())
				.then((data) => {
					this.spaces = [{ id: "", name: " -- اختر المساحة  --" }, ...data];
				});
		},
		getUsers() {
			fetch("/api/users/", {
				method: "GET",
				credentials: "include",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFToken": csrf_token,
				},
			})
				.then((response) => response.json())
				.then((data) => {
					this.users = [...this.users, ...data];
				});
		},
		getSpaceTools(event) {
			this.spaceUnits = [];
			fetch(
				`/api/spaces/${event.target.value}/tools?user_id=${this.selectedUserId}`
			)
				.then((response) => response.json())
				.then((data) => {
					this.tools = [...data];
				});
			this.selectedSpace = this.spaces.filter(
				(space) => space.id === Number(event.target.value)
			)[0];
			this.selectedSpace.cat_prices &&
				this.selectedSpace.cat_prices.forEach((price) => {
					this.spaceUnits.push(price);
				});
			this.spaceUnits = [
				...new Map(
					this.spaceUnits.map((item) => [item["unit_id"], item])
				).values(),
			];
			this.selectedUnit = this.spaceUnits[0];
			this.fromTimeRange = this.getFromTimeList(
				10,
				18 - this.getBoundaryTime()
			);
		},
		changeUnit: function (event) {
			this.selectedUnit = this.spaceUnits.filter(
				(unit) => Number(event.target.value) === unit.unit_id
			)[0];
			if (this.selectedUnit.unit_id === 0) {
				this.fromTime = "";
				this.toTime = "";
				this.toTimeRange = [];
				this.fromTimeRange = this.getFromTimeList(
					10,
					18 - this.getBoundaryTime()
				);
			} else if (this.selectedUnit.unit_id === 1) {
				this.fromTime = "";
				this.toTime = "";
				this.isDatepickerShow = true
			}
		},
		getFromTimeList(start, end) {
			this.toTimeRange = [{ value: "", text: " إلى " }];
			let timeList = [{ value: "", text: " من " }];
			for (i = start; i <= end; i++) {
				val = i;
				option = i;
				pm_am = " ص";
				if (i > 12) {
					option -= 12;
					pm_am = " م";
				} else if (i == 12) {
					pm_am = " م";
				}
				timeList.push({
					value: val,
					text: option + ":00" + pm_am,
				});
				if (val < end) {
					timeList.push({
						value: val + 0.5,
						text: option + ":30" + pm_am,
					});
				}
			}
			return timeList;
		},
		getToTimeList(start, end) {
			if (this.fromTime === "") {
				this.toTime = "";
				this.toTimeRange = [{ value: "", text: " إلى " }];
			} else {
				this.toTimeRange = [];
				let timeList = [];
				const selectCategoryPrices =
					this.selectedSpace.cat_prices &&
					this.selectedSpace.cat_prices.filter((price) => {
						return price.unit_id === this.selectedUnit.unit_id;
					});
				let option;
				selectCategoryPrices.forEach((price) => {
					option = price.unit_value + Number(start);
					let pm_am = " ص";
					if (price.unit_value + Number(start) > 12.5) {
						option -= 12;
						pm_am = " م";
					} else if (
						price.unit_value + Number(start) === 12 ||
						price.unit_value + Number(start) === 12.5
					) {
						pm_am = " م";
					}
					if (price.unit_value + Number(start) <= end) {
						timeList.push({
							value: price.unit_value + Number(start),
							text:
								(price.unit_value + Number(start)) % 1 === 0
									? option + ":00" + pm_am
									: option - 0.5 + ":30" + pm_am,
						});
					}
					this.toTime = timeList[0].value;
				});
				this.toTimeRange = timeList;
			}
		},
		getBoundaryTime() {
			let unitValues = [];
			this.selectedSpace
				? this.selectedSpace.cat_prices.forEach((price) => {
						unitValues.push(price.unit_value);
				  })
				: 0;
			return Math.min(...unitValues);
		},
		getReservedDays() {
			if (!this.selectedSpace.id) {
				return;
			}
			let data
			if (this.selectedUnit.unit_id === 0) {
				data = {
				from_time:
					this.fromTime % 1 === 0
						? new Date(Date.UTC(0, 0, 0, this.fromTime, 0, 0)).toJSON()
						: new Date(Date.UTC(0, 0, 0, this.fromTime - 0.5, 30, 0)).toJSON(),
				to_time:
					this.toTime % 1 === 0
						? new Date(Date.UTC(0, 0, 0, this.toTime, 0, 0)).toJSON()
						: new Date(Date.UTC(0, 0, 0, this.toTime - 0.5, 30, 0)).toJSON(),
			};
			} else if (this.selectedUnit.unit_id === 1) {
				data = {
					days_only : true
				}
			}
			
			fetch(`/api/spaces/${this.selectedSpace.id}/reserved-days/`, {
				method: "POST",
				credentials: "include",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFToken": csrf_token,
				},
				body: JSON.stringify(data),
			})
				.then((response) => response.json())
				.then((data) => {
					$("#datepicker").datepicker("destroy");
					$("#datepicker")
						.datepicker({
							format: "yyyy-mm-dd",
							startDate: "+2d",
							endDate: "+3m",
							todayBtn: true,
							clearBtn: true,
							language: "ar",
							multidate: true,
							multidateSeparator: ",",
							daysOfWeekDisabled: "",
							daysOfWeekHighlighted: "5,6",
							title: "إختر أيام الحجز",
							// todayHighlight: true,
							datesDisabled: [...data],
							rtl: true,
						})
						.on("changeDate", function (e) {
							app.dates = [...e.dates];
							app.calculate();
						});
				});
		},
		calculate() {
			if (!this.selectedUserId) {
				return;
			}
			let data = {
				days: this.dates.length,
				space_price_id: this.selectedUnit.unit_id === 0
						? this.selectedSpace.cat_prices.filter(
								(price) => price.unit_value === this.toTime - this.fromTime
							)[0].id
						: this.selectedUnit.unit_id === 1 
						&& this.selectedSpace.cat_prices.filter(
								(price) => price.unit_id === 1
							)[0].id
						,
				tool_ids: [...this.tool_ids],
			};
			fetch(
				`/api/spaces/${this.selectedSpace.id}/calculate-price?user_id=${this.selectedUserId}`,
				{
					method: "POST",
					credentials: "include",
					headers: {
						"Content-Type": "application/json",
						"X-CSRFToken": csrf_token,
					},
					body: JSON.stringify(data),
				}
			)
				.then((response) => response.json())
				.then((res) => (this.price_table = [...res]));
		},
		submitForm() {
			const from_time = 
					this.fromTime && this.selectedUnit.unit_id === 0
						? this.fromTime % 1 === 0
							? new Date(Date.UTC(0, 0, 0, this.fromTime, 0, 0)).toJSON()
							: new Date(Date.UTC(0, 0, 0, this.fromTime - 0.5, 30, 0)).toJSON()
						: null
			const to_time = 
					this.toTime && this.selectedUnit.unit_id === 0
						? this.toTime % 1 === 0
							? new Date(Date.UTC(0, 0, 0, this.toTime, 0, 0)).toJSON()
							: new Date(Date.UTC(0, 0, 0, this.toTime - 0.5, 30, 0)).toJSON()
						: null
			let data = {
				description: this.description,
				attendance_num: this.attendance_num,
				min_age: this.min_age,
				max_age: this.max_age,
				space_id: this.selectedSpace.id,
				space_price_id: this.selectedUnit.unit_id === 0
					? this.selectedSpace.cat_prices.filter((price) => {
						return (
							price.unit_value === this.toTime - this.fromTime &&
							price.unit_id === this.selectedUnit.unit_id
						)
					})[0].id
						: this.selectedUnit.unit_id === 1 
						&& this.selectedSpace.cat_prices.filter((price) => {
						return (
							price.unit_id === this.selectedUnit.unit_id
						)
					})[0].id,
				tools: [...this.tool_ids],
				days_only:
					this.selectedUnit.unit_id === 0
						? false
						: this.selectedUnit.unit_id === 1
						? true
						: false,
				days: this.dates,	
				payment_status: this.payment_status,
			};
			if (from_time && to_time) {
				data = { ...data, from_time, to_time}
			}
			fetch(`/api/spaces/reserve?user_id=${this.selectedUserId}`, {
				method: "POST",
				credentials: "include",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFToken": csrf_token,
				},
				body: JSON.stringify(data),
			})
				.then((response) => response.json())
				.then((res) => {
					Toastify({
						text: res.message,
						duration: 3000,
						newWindow: true,
						close: true,
						gravity: "top", 
						position: "left",
						stopOnFocus: true,
						style: {
							background: "linear-gradient(to right, #00b09b, #96c93d)",
						},
						onClick: function () {
							window.location.href = res.space_reservation_url;
						} 
					}).showToast();
				});
		},
	},
	delimiters: ["{", "}"],
}).mount("#app");
