---
layout: post
title: "[AI SCHOOL 5기] SQL 프로그래밍"
date: 2022-04-11 19:52:00 +0900
categories: [Study, AI SCHOOL]
tags: [AI SCHOOL, 멋쟁이사자처럼, 코드라이언, DB, SQL]
slug: aischool-05-00-sql-programming
---

# DBMS
- DataBase Management System
- 하드웨어에 저장된 데이터베이스를 관리해주는 소프트웨어
- 관계형 데이터베이스(RDBMS)가 주로 사용
- Oracle, MySQL(MariaDB), SQLite, MS SQL, PstgreSQL

---

# 데이터 모델링
1. 현실 세계
2. E-R 다이어그램 (개념 스키마)
3. Relation 모델 (논리적 스키마)
4. 물리적인 SQL 코드 (데이터베이스 스키마)

## 개념적 데이터 모델링
- 현실 세계로부터 개체를 추출, 개체들의 관계를 정의, E-R 다이어그램 생성
- 개체(Entity): 회원, 제품 등 저장할 가치가 있는 데이터를 포함한 개체
- 속성(Attribute): 이름, 이메일 등 의미 있는 데이터의 가장 작은 논리적 단위
- 관계(Relationship): 구매 등 개체와 개체 사이의 연관성 및 개체 집합 간 대응 관계

## 논리적 데이터 모델링
- E-R 다이어그램을 바탕으로 논리적인 구조를 Relation 모델로 표현
- 릴레이션(Relation): 개체에 대한 데이터를 2차원 테이블 구조로 표현한 것
- 속성(Attribute): 열, 필드
- 튜플(Tuble): 행, 레코드, 인스턴스
- 차수(Degree): 릴레이션 내 속성(Column)의 총 개수
- 카디널리티(Cardinality): 릴레이션 내 튜플(Row)의 총 개수

## 물리적 데이터 모델링
- Relation 모델을 물리 저장 장치에 저장할 수 있는 물리적 구조로 구현

---

# SQL
- Structured Query Language
- RDBMS에서 데이터를 관리 및 처리하기 위해 만들어진 언어
- DDL(Data Definition Language): CREATE, ALTER, DROP
- DML(Data Manipulation Language): SELECT, INSERT, UPDATE, DELETE
- DCL(Data Control Language): GRANT, REVOKE

---

# NoSQL
- 관계형 모델을 사용하지 않음, 명시적인 스키마가 없음
- 대용량 데이터 분산 저장에 특화
- Kye-Value, Document, Wide Column, Graph 등