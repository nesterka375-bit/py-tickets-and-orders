from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from typing import List, Dict, Optional
from db.models import Order, Tickets, MovieSession

User = get_user_model()


def create_order(tickets: List[Dict], username: str, date: Optional[str] = None) -> Order:
	with transaction.atomic():
		user = User.objects.get(username=username)
		order = Order(user=user)
		if date:
			order.created_at = date
		order.save()
		for ticket_data in tickets:
			movie_session = MovieSession.objects.get(pk=ticket_data["movie_session"])
			Tickets.objects.create(
				order=order,
				row=ticket_data["row"],
				seat=ticket_data["seat"],
				movie_session=movie_session
			)
		return order


def get_orders(username: Optional[str] = None) -> QuerySet:
	if username:
		return Order.objects.filter(user__username=username)
	return Order.objects.all()