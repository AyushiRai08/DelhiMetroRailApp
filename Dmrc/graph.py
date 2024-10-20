import heapq
from collections import defaultdict, deque

class Graph:
    class Vertex:
        def __init__(self):
            self.nbrs = {}

    def __init__(self):
        self.vtces = {}

    def num_vertices(self):
        return len(self.vtces)

    def contains_vertex(self, vname):
        return vname in self.vtces

    def add_vertex(self, vname):
        self.vtces[vname] = self.Vertex()

    def remove_vertex(self, vname):
        if vname in self.vtces:
            vtx = self.vtces[vname]
            for key in list(vtx.nbrs.keys()):
                self.vtces[key].nbrs.pop(vname, None)
            del self.vtces[vname]

    def num_edges(self):
        count = sum(len(vtx.nbrs) for vtx in self.vtces.values())
        return count // 2

    def contains_edge(self, vname1, vname2):
        return vname1 in self.vtces and vname2 in self.vtces[vname1].nbrs

    def add_edge(self, vname1, vname2, value):
        if vname1 in self.vtces and vname2 in self.vtces and vname2 not in self.vtces[vname1].nbrs:
            self.vtces[vname1].nbrs[vname2] = value
            self.vtces[vname2].nbrs[vname1] = value

    def remove_edge(self, vname1, vname2):
        if self.contains_edge(vname1, vname2):
            self.vtces[vname1].nbrs.pop(vname2, None)
            self.vtces[vname2].nbrs.pop(vname1, None)

    def display_map(self):
        print("\tDelhi Metro Map")
        print("\t------------------")
        for key in self.vtces:
            vtx = self.vtces[key]
            print(f"{key} => {', '.join(f'{nbr}: {vtx.nbrs[nbr]}' for nbr in vtx.nbrs)}")
        print("\t------------------")

    def display_stations(self):
        print("\nStations in the Map:")
        for i, key in enumerate(self.vtces.keys(), 1):
            print(f"{i}. {key}")

    def has_path(self, vname1, vname2, processed):
        if self.contains_edge(vname1, vname2):
            return True
        processed.add(vname1)

        for nbr in self.vtces[vname1].nbrs:
            if nbr not in processed and self.has_path(nbr, vname2, processed):
                return True

        return False

    def dijkstra(self, src, des, include_time):
        pq = []
        distances = {key: float('inf') for key in self.vtces}
        distances[src] = 0
        heapq.heappush(pq, (0, src))

        while pq:
            curr_cost, curr_vertex = heapq.heappop(pq)

            if curr_vertex == des:
                return curr_cost

            for neighbor, weight in self.vtces[curr_vertex].nbrs.items():
                if include_time:
                    new_cost = curr_cost + weight + 120 + 40 * weight
                else:
                    new_cost = curr_cost + weight

                if new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    heapq.heappush(pq, (new_cost, neighbor))

        return distances[des]

    def get_minimum_distance(self, src, dst):
        return self.dijkstra(src, dst, include_time=False)

    def get_minimum_time(self, src, dst):
        return self.dijkstra(src, dst, include_time=True)

    def create_metro_map(self):
        stations = [
            ("Noida Sector 62~B", 8),
            ("Botanical Garden~B", 10),
            ("Yamuna Bank~B", 8),
            ("Rajiv Chowk~BY", 6),
            ("Vaishali~B", 9),
            ("Moti Nagar~B", 7),
            ("Janak Puri West~BO", 6),
            ("Dwarka Sector 21~B", 15),
            ("Huda City Center~Y", 6),
            ("Saket~Y", 7),
            ("Vishwavidyalaya~Y", 5),
            ("Chandni Chowk~Y", 2),
            ("New Delhi~YO", 1),
            ("AIIMS~Y", 7),
            ("Shivaji Stadium~O", 2),
            ("DDS Campus~O", 7),
            ("IGI Airport~O", 8),
            ("Rajouri Garden~BP", 2),
            ("Netaji Subhash Place~PR", 3),
            ("Punjabi Bagh West~P", 2)
        ]

        for station in stations:
            self.add_vertex(station[0])

        edges = [
            ("Noida Sector 62~B", "Botanical Garden~B", 8),
            ("Botanical Garden~B", "Yamuna Bank~B", 10),
            ("Yamuna Bank~B", "Rajiv Chowk~BY", 6),
            ("Rajiv Chowk~BY", "Moti Nagar~B", 9),
            ("Moti Nagar~B", "Janak Puri West~BO", 7),
            ("Janak Puri West~BO", "Dwarka Sector 21~B", 6),
            ("Huda City Center~Y", "Saket~Y", 15),
            ("Saket~Y", "AIIMS~Y", 6),
            ("AIIMS~Y", "Rajiv Chowk~BY", 7),
            ("Rajiv Chowk~BY", "New Delhi~YO", 1),
            ("New Delhi~YO", "Chandni Chowk~Y", 2),
            ("Chandni Chowk~Y", "Vishwavidyalaya~Y", 5),
            ("New Delhi~YO", "Shivaji Stadium~O", 2),
            ("Shivaji Stadium~O", "DDS Campus~O", 7),
            ("DDS Campus~O", "IGI Airport~O", 8),
            ("Moti Nagar~B", "Rajouri Garden~BP", 2),
            ("Punjabi Bagh West~P", "Rajouri Garden~BP", 2),
            ("Punjabi Bagh West~P", "Netaji Subhash Place~PR", 3)
        ]

        for edge in edges:
            self.add_edge(edge[0], edge[1], edge[2])

def main():
    g = Graph()
    g.create_metro_map()

    while True:
        print("\t\t\t\t~~LIST OF ACTIONS~~\n")
        print("1. LIST ALL THE STATIONS IN THE MAP")
        print("2. SHOW THE METRO MAP")
        print("3. GET SHORTEST DISTANCE FROM A 'SOURCE' STATION TO 'DESTINATION' STATION")
        print("4. GET SHORTEST TIME TO REACH FROM A 'SOURCE' STATION TO 'DESTINATION' STATION")
        print("5. EXIT")

        choice = int(input("\nENTER YOUR CHOICE FROM THE ABOVE LIST (1 to 5): "))

        if choice == 5:
            break

        if choice == 1:
            g.display_stations()
        elif choice == 2:
            g.display_map()
        elif choice in (3, 4):
            src = input("ENTER THE SOURCE STATION: ")
            dst = input("ENTER THE DESTINATION STATION: ")

            if choice == 3:
                distance = g.get_minimum_distance(src, dst)
                print(f"SHORTEST DISTANCE FROM {src} TO {dst} IS {distance} KM")
            elif choice == 4:
                time = g.get_minimum_time(src, dst)
                print(f"SHORTEST TIME FROM {src} TO {dst} IS {time // 60} MINUTES")
        else:
            print("Please enter a valid option!")

if __name__ == "__main__":
    main()
