import traceback

if __name__ == '__main__':
    try:
        from jamaalca import JamaAlca
        app = JamaAlca()
        app.mainloop()
    except Exception:
        traceback.print_exc()
        raise
