from NAryMatrixClass import NAryMatrixRelation
from DpopUtilsClass import join, projection, find_arg_optimal


class Dpop(object):

    def __init__(self, pseudoTree):
        self.PseudoTree = pseudoTree

    def Solve_Problem(self):
        # Util message propagation
        # print('-----------------------')
        # print('UTIL PROPAGATION')
        # print('-----------------------')
        util_message = self.Get_Utils(self.PseudoTree.root, self.PseudoTree.root.get_Child())
        optimal_util_value, optimal_util = find_arg_optimal(self.PseudoTree.root.var, util_message)

        self.PseudoTree.root.var.optimal_value = optimal_util

        # print('-----------------------')
        # print('VALUE PROPAGATION')
        # print('-----------------------')
        # Value message propagation
        self.SendValue(self.PseudoTree.root, optimal_util, self.PseudoTree.root.get_AllChilds())

        # print('************************')
        # print('RESULT')
        # print('************************')
        # Show results
        meetings_hours = {}
        for node in self.PseudoTree.PseudoNodes:
            meetings_hours[node.var.name.split("_")[1]] = node.var.optimal_value
            # print(node.var.name + ' ' + node.var.optimal_value)
        for meeting, time in meetings_hours.items():
            print(meeting, '->', time)


    def Get_Utils(self, parent, nodesToloop):
        utilsFromChildrensArray = []
        # print('Calculating Utils for :: ' + parent.name + ' with nodesToloop :: ', end = '' )
        # print([c.name for c in parent.get_Child()]  )


        for node in nodesToloop:
            if node.get_Child():  # if node has childs get deeper
                util = self.Get_Utils(node, node.get_Child())
            else:
                util = self.CalculateUtil(node)  # return util for the leaf node
            parent.utilsFromChildrensArray.append(util)
            #utilsFromChildrensArray.append(util)
        if parent.is_root:
            return self._joinUtilMessagesList(parent.utilsFromChildrensArray)

        return self.CalculateUtil(parent, parent.utilsFromChildrensArray)

    def SendValue(self, sender, util, nodesToLoop):
        for node in nodesToLoop:
            # print("VALUE: [" + sender.name + '] -> [' + node.name + '] :: ' + util)
            node.ValueMessages[sender.name] = util

            for i in sender.ValueMessages.keys():
                    for v in node.Join.dimensions():
                        if i == v.name:
                            node.ValueMessages[i] = sender.ValueMessages[i]

        for node in sender.get_Child():

            new_util = self.HandleValue(node)
            self.SendValue(node, new_util, node.get_AllChilds())

    def HandleValue(self, node):
        # print('-----------------------')
        # print("[HANDLE] VALUES: " + node.name)
        # print('Received : ', end='')
        # print(node.ValueMessages)
        # print('JOIN     : ' , end='')
        # print([v.name for v in node.Join.dimensions()])
        rel = node.Join.slice(node.ValueMessages)
        # print(rel._m)
        values, current_cost = find_arg_optimal(node.var, rel)
        node.var.optimal_value = current_cost
        return current_cost

    def CalculateUtil(self, node, utils_to_join = []):
        # print('UTIL : ' + node.name)
        for sep in node.get_AllParents():
            variables, constraint = node.compute_binary_constraint(sep)
            constraintArray = NAryMatrixRelation(variables, constraint, name='UTIL_' + node.name + '_' + sep.name)
            ##utils_to_join.append(constraintArray)
            node.utilsFromChildrensArray.append(constraintArray)

        # print('seperators computed')

        ##util_message = self._joinUtilMessagesList(utils_to_join)
        util_message = self._joinUtilMessagesList(node.utilsFromChildrensArray)

        node.Join = util_message


        # print('utils_to_join = ', end='')
        # print([v.name for v in node.utilsFromChildrensArray])
        # print([v.name for v in util_message.dimensions()])

        util_message = projection(util_message, node.var, name = util_message.name)

        return util_message

    def _joinUtilMessagesList(self, utils_to_join):
        # print('TO JOIN :: ' + str(len(utils_to_join)) + ' messages.')

        util_message = utils_to_join.pop(0)

        for u in utils_to_join:

            # print('computing...')
            # print('U1 dimensions = ', end='')
            # print([v.name for v in util_message.dimensions()])
            # print('U2 dimensions = ', end='')
            # print([v.name for v in u.dimensions()])

            util_message = join(util_message, u)


        return util_message
