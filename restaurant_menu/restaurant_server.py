__author__ = 'naren'
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from restaurant_db import Base, Restaurant
import traceback

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurants = self.get_restaurants()
                output = ""
                output += "<html><body>"
                output += "<h1><a href='/restaurants/new'>Create New restaurant here</a></h1>"
                for restaurant in restaurants:
                    output += restaurant[0] + "</br>"
                    output += "<a href='/restaurants/{0}/edit'>Edit</a></br><a href='/restaurants/{1}/delete'>" \
                              "Delete</a> </br> </br>".format(restaurant[1], restaurant[1])
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Enter the name for
                new restaurant</h2><input name="name" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                res_id = str(self.path).split('/')[2]
                res_name = self.get_name_from_id(res_id)
                output = ""
                output += "<html><body>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/{0}/edit'>
                <h2>Rename the restaurant : {1} </h2><input name="name" type="text" placeholder={1}><input type="submit" value="Rename">
                </form>'''.format(res_id, res_name)
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                res_id = str(self.path).split('/')[2]
                res_name = self.get_name_from_id(res_id)
                output = ""
                output += "<html><body>"
                output += "<h1> Are you sure want to delete : {0} </h1>".format(res_name)
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/{0}/delete'>
                <input type="submit" value="Delete !!!"></form>'''.format(res_id)
                # class="float-left submit-button" >Delete</button>'''.format(res_id)
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype,  pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('name')
                self.create_restaurant(messagecontent[0])
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return

            if self.path.endswith("/edit"):
                ctype,  pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                res_id = str(self.path).split('/')[2]
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('name')
                res_id = str(self.path).split('/')[2]
                self.rename_restaurant(res_id, messagecontent[0])
                print "Restaurant renamed"
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return

            if self.path.endswith("/delete"):
                print "Got POST for delete"
                ctype,  pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                res_id = str(self.path).split('/')[2]
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('name')
                res_id = str(self.path).split('/')[2]
                self.delete_restaurant(res_id)
                print "Restaurant deleted"
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return
        except:
            pass

    def get_restaurants(self):
        session = DBSession()
        return session.query(Restaurant.name, Restaurant.id).all()

    def create_restaurant(self, res_name):
        session = DBSession()
        new_restaurant = Restaurant(name=res_name)
        session.add(new_restaurant)
        session.commit()
        session.close()

    def get_name_from_id(self, res_id):
        session = DBSession()
        q_name = session.query(Restaurant.name).filter(Restaurant.id == res_id).first()
        if q_name:
            session.close()
            return q_name[0]
        session.close()
        return ""

    def delete_restaurant(self, res_id):
        try:
            session = DBSession()
            q_res = session.query(Restaurant).filter(Restaurant.id == res_id).first()
            session.delete(q_res)
            session.commit()
            session.close()
        except:
            print traceback.format_exc()

    def rename_restaurant(self, res_id, new_name):
        try:
            session = DBSession()
            q_rename = session.query(Restaurant).filter(Restaurant.id == res_id).first()
            session.close()
            if q_rename:
                q_rename.name = new_name
                session.add(q_rename)
                session.commit()
            return
        except:
            print traceback.format_exc()



def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
