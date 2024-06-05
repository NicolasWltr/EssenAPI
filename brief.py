from flask import Flask, render_template, request, redirect, url_for


def init(app):
    @app.route('/brief')
    def brief():
        return render_template('brief.html')