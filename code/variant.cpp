#include <memory>
#include <variant>

struct Expr;
struct Neg { std::shared_ptr<Expr> expr; };
struct Add { std::shared_ptr<Expr> lhs, rhs; };
struct Mul { std::shared_ptr<Expr> lhs, rhs; };
struct Expr : std::variant<int, Neg, Add, Mul> { using variant::variant; };

namespace std {
    template <>
    struct variant_size<Expr> : variant_size<Expr::variant> {};

    template <std::size_t I>
    struct variant_alternative<I, Expr> : variant_alternative<I, Expr::variant> {};
}

int eval(const Expr& expr) {
  struct visitor {
    int operator()(int i) const {
      return i;
    }
    int operator()(const Neg& n) const {
      return -eval(*n.expr);
    }
    int operator()(const Add& a) const {
      return eval(*a.lhs) + eval(*a.rhs);
    }
    int operator()(const Mul& m) const {
      // Optimize for multiplication by 0
      if(int * lhsInt = std::get_if<int>(m.lhs.get()); lhsInt && *lhsInt == 0)
        return 0;
      if(int * rhsInt = std::get_if<int>(m.rhs.get()); rhsInt && *rhsInt == 0)
        return 0;

      return eval(*m.lhs) * eval(*m.rhs);
    }
  };
  return std::visit(visitor{}, expr);
}


int main() 
{
}
