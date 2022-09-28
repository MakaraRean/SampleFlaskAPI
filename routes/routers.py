from fastapi import APIRouter

user = APIRouter( tags=['User'])
pos = APIRouter(prefix='/cp', tags=['Pos'])
product = APIRouter(tags=['Product'])
product_type = APIRouter(prefix='/cp', tags=['Product type'])
dashboard = APIRouter(prefix='/cp', tags=['Dashboard'])